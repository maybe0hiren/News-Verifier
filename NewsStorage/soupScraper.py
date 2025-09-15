import os
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import requests
from databaseManager import addPair

url = "https://www.brut.media/in"
storage = "NewsStorage/images"
os.makedirs(storage, exist_ok=True)

options = Options()
options.headless = True  # Set False to see Chrome UI
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(8)  # Wait for page content to load

# Scroll down multiple times to load more media
for _ in range(10):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(1.5)

media_cards = driver.find_elements(By.CSS_SELECTOR, "article, div[data-testid]")

def hash_image(path):
    with Image.open(path) as img:
        img = img.convert('RGB').resize((128,128))
        return hashlib.md5(img.tobytes()).hexdigest()

observed_hashes = set()
image_count = 0

for card in media_cards:
    try:
        img_elem = card.find_element(By.TAG_NAME, "img")
        img_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
        if not img_url:
            continue

        # Extract caption from first p, h2, or span inside media card
        try:
            caption = card.find_element(By.CSS_SELECTOR, "p, h2, span").text.strip()
        except:
            caption = "No caption"
        if not caption:
            caption = "No caption"

        # Download image
        image_path = os.path.join(storage, f"brut_img_{image_count}.jpg")
        img_data = requests.get(img_url, timeout=10).content
        with open(image_path, "wb") as f:
            f.write(img_data)

        # Hash the image for deduplication
        h = hash_image(image_path)
        if h in observed_hashes:
            os.remove(image_path)
            continue
        observed_hashes.add(h)

        # Save path and caption to DB
        addPair(image_path, caption)

        print(f"Saved entry #{image_count + 1}: hash={h}")
        print(f"Caption: {caption}")
        print(f"Image path: {image_path}\n")

        image_count += 1
        time.sleep(1)
    except Exception as e:
        print(f"Error processing entry #{image_count + 1}: {e}")

print("Scraping complete. Browser will stay open until you press Enter.")
input()
driver.quit()
