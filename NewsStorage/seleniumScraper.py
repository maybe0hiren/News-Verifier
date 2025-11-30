import os
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from PIL import Image
import requests
from databaseManager import addPair

# Hash an image file for deduplication
def hash_image(path):
    with Image.open(path) as img:
        img = img.convert('RGB').resize((128, 128))
        return hashlib.md5(img.tobytes()).hexdigest()


options = Options()
options.page_load_strategy = "eager"
options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.images": 2
})
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)
driver.set_script_timeout(60)

try:
    driver.get('https://timesofindia.indiatimes.com/')
except TimeoutException:
    print("Page load timed out but continuing...")

time.sleep(3)

# Scroll several times to ensure images load
for _ in range(10):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# Find all image elements on page
img_elements = driver.find_elements(By.TAG_NAME, 'img')
observed_hashes = set()
temp_dir = 'images'
os.makedirs(temp_dir, exist_ok=True)

# Process each image element
for idx, img in enumerate(img_elements):
    img_url = img.get_attribute('src')
    if not img_url:
        continue
    img_path = os.path.join(temp_dir, f'toi_{idx}.jpeg')
    try:
        # Download image with timeout
        r = requests.get(img_url, timeout=10)
        with open(img_path, 'wb') as f:
            f.write(r.content)
        # Compute hash to avoid duplicates
        h = hash_image(img_path)
        if h in observed_hashes:
            os.remove(img_path)
            continue
        observed_hashes.add(h)
        # Extract caption from alt or parent text
        caption = img.get_attribute('alt') or ''
        try:
            parent = img.find_element(By.XPATH, '..')
            caption = caption or parent.text
            caption = caption.replace("Article image for: ", "")
        except Exception:
            pass
        # Save image path using your DB function
        addPair(img_path, caption)
        print(f"Saved: {img_path} | Caption: {caption}")
        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"Image '{img_path}' deleted successfully.")
        else:
            print(f"Image '{img_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

# Cleanup temporary images
for f in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, f))
os.rmdir(temp_dir)
driver.quit()
