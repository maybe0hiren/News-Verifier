from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, os, time
import hashlib
from databaseManager import addPair

def file_hash(data):
    return hashlib.md5(data).hexdigest()
seen_hashes = set()

storage = "NewsStorage/images"
os.makedirs(storage, exist_ok=True)

driver = webdriver.Chrome()
driver.get("WEBSITE HERE")
time.sleep(20)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.TAG_NAME, "img"))
)
images = driver.find_elements(By.TAG_NAME, "img")
print(f"Found {len(images)} images")

for i, img in enumerate(images):
    time.sleep(1)
    src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("data-srcset")
    print(f"[{i}] src={src}")
    if not src:
        continue
    try:
        imageData = requests.get(src).content
        h = file_hash(imageData)
        if h in seen_hashes:
            print(f"Skipping duplicate: {src}")
            continue
        seen_hashes.add(h)
        imagePath = os.path.join(storage, f"image{i}.jpg")
        with open(imagePath, "wb") as f:
            f.write(imageData)
        print(f"Downloaded image {i} -> {imagePath}")
        caption = None
        try:
            headline = img.find_element(By.XPATH, "ancestor::a")
            caption = headline.text.strip()
        except:
            pass
        if not caption:
            try:
                container = img.find_element(By.XPATH, "ancestor::div[1]")
                caption = container.text.strip()
            except:
                pass
        if not caption:
            caption = img.get_attribute("alt") or img.get_attribute("title")
        if not caption:
            caption = "No caption"
        print(f"Associated headline: {caption}")

        addPair(imagePath, caption)
    except Exception as e:
        print(f"Error with {src}: {e}")

driver.quit()
