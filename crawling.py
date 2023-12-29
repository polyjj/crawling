from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os

# Set up Chrome driver with automatic management
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def scroll_to_load_images(driver, num_images):
    """
    Scroll the webpage to load more images.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # Wait for images to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        if len(driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')) >= num_images:
            break

def download_images(query, num_images):
    base_url = 'https://www.google.com'
    url = f"{base_url}/search?q={query}&source=lnms&tbm=isch"
    
    driver.get(url)
    scroll_to_load_images(driver, num_images)

    images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')
    unique_images = set()

    download_path = 'C:\\Users\\'  # Set your desired download path here

    for i, img in enumerate(images):
        if len(unique_images) >= num_images:
            break

        try:
            img_url = img.get_attribute('src')

            if img_url and img_url.startswith('http') and img_url not in unique_images:
                unique_images.add(img_url)
                img_data = urllib.request.urlopen(img_url).read()
                file_path = os.path.join(download_path, f'{query}_{len(unique_images)-1}.jpg')
                with open(file_path, 'wb') as file:
                    file.write(img_data)

        except Exception as e:
            print(f"Error downloading image {i}: {e}")

    driver.quit()

# Example usage
download_images('임시완', 45)