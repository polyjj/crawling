from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def download_images(query, num_images):
    base_url = 'https://www.google.com'
    url = f"{base_url}/search?q={query}&source=lnms&tbm=isch"
    
    driver.get(url)

    images_downloaded = 0
    image_index = 0
    download_path = 'C:\\Users\\82103\\downloaded_images\\'  # 다운로드 경로 설정

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    while images_downloaded < num_images:
        try:
            # 이미지 목록에서 이미지 찾기
            images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')
            if image_index < len(images):
                # 이미지 클릭
                actions = ActionChains(driver)
                actions.move_to_element(images[image_index]).click().perform()
                time.sleep(2)  # 이미지 로드를 기다림

                # 큰 이미지 URL 가져오기
                large_image_xpath = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
                large_images = driver.find_elements(By.XPATH, large_image_xpath)
                if not large_images:
                    large_images = driver.find_elements(By.XPATH, '//img[contains(@class,"n3VNCb")]')
                
                for img in large_images:
                    if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                        img_url = img.get_attribute('src')
                        # 이미지 다운로드
                        img_data = urllib.request.urlopen(img_url).read()
                        file_path = os.path.join(download_path, f'{query}_{images_downloaded}.jpg')
                        with open(file_path, 'wb') as file:
                            file.write(img_data)
                        images_downloaded += 1
                        if images_downloaded >= num_images:
                            break

            image_index += 1

        except Exception as e:
            print(f"Error downloading image {image_index}: {e}")

    driver.quit()

# 예제 사용
download_images('이승기', 45)