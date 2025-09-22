import os
import time
import hashlib
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from PIL import Image
import requests

# Hash an image file for deduplication
def hash_image(path):
    with Image.open(path) as img:
        img = img.convert('RGB').resize((128, 128))
        return hashlib.md5(img.tobytes()).hexdigest()

# Insert or ignore data into your storage table with hash + captions
def save_to_db(h, captions):
    db_name = "NewsStorage/storage.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        # Prepare columns and placeholders for insert
        columns = ["hash"] + [f"caption{i}" for i in range(1, 51)]
        placeholders = ", ".join(["?"] * len(columns))
        sql = f"INSERT OR IGNORE INTO storage ({', '.join(columns)}) VALUES ({placeholders})"
        # Create a tuple with hash + 50 captions (use empty strings if fewer given)
        data = (h,) + tuple(captions[:50] + [""] * (50 - len(captions)))
        cursor.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

# Setup Chrome WebDriver with longer page load timeout
driver = webdriver.Chrome()
driver.set_page_load_timeout(300)

try:
    driver.get('https://timesofindia.indiatimes.com/')
except TimeoutException:
    print("Page load timed out but continuing...")

time.sleep(3)

# Scroll to load images
for _ in range(10):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

img_elements = driver.find_elements(By.TAG_NAME, 'img')
observed_hashes = set()
temp_dir = 'tmp_images'
os.makedirs(temp_dir, exist_ok=True)

for idx, img in enumerate(img_elements):
    img_url = img.get_attribute('src')
    if not img_url:
        continue
    img_path = os.path.join(temp_dir, f'toi_{idx}.jpg')
    try:
        r = requests.get(img_url, timeout=10)
        with open(img_path, 'wb') as f:
            f.write(r.content)
        h = hash_image(img_path)
        if h in observed_hashes:
            os.remove(img_path)
            continue
        observed_hashes.add(h)
        caption = img.get_attribute('alt') or ''
        try:
            parent = img.find_element(By.XPATH, '..')
            caption = caption or parent.text
        except Exception:
            pass
        # Example: fill all caption columns with the same caption for demo
        captions_list = [caption] * 50
        save_to_db(h, captions_list)
        print(f"Saved to DB: hash={h} | Caption preview: {caption[:50]}")
    except Exception as e:
        print(f"Error: {e}")

# Cleanup temporary files
for f in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, f))
os.rmdir(temp_dir)
driver.quit()
