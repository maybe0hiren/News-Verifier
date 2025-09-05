import requests
from bs4 import BeautifulSoup
import os
import time
from accessDB import addPair
url = "WEBSITE HERE"
storage = "NewsStorage/images"
os.makedirs(storage, exist_ok=True)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
images = soup.find_all("img")

for i, img in enumerate(images):
    imageURL = img.get("src")
    if imageURL.startswith("//"):
        imageURL = "https:" + imageURL
    elif imageURL .startswith("/"):
        imageURL = URL.rstrip("/") + imageURL
    
    imageStorePath = os.path.join(storage, f"img{i}.jpg")
    try:
        imageData = requests.get(imageURL).content
        with open(imageStorePath, "wb") as f:
            f.write(imageData)
        print("Image downloaded...")
        addPair(imageStorePath)
    except Exception as e:
        print(f"ERROE: {e}")
    time.sleep(1)
    
