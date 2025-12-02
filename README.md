# TrueTrace – AI-Powered News Verifier
A lightweight system that verifies whether a user-submitted news caption accurately describes an uploaded image, helping combat misinformation spread on social media.

---

## 📌 Overview
TrueTrace is an AI-powered tool designed to assist users in verifying online news articles and social-media posts. The system evaluates the relationship between an uploaded image and a caption by combining perceptual hashing, web scraping, semantic embeddings, cosine similarity, and a Large Language Model for detailed analysis.

Users interact with a simple web interface where they upload an image and provide the caption they want to verify. TrueTrace then retrieves relevant news data from the web, compares semantic similarity using transformer-based embeddings, and generates a human-readable report explaining whether the caption is accurate, misleading, or out of context.

---

## ✨ Features
- **Perceptual Hashing (pHash)** for detecting duplicate or visually similar images  
- **Web Scraping (Selenium + BeautifulSoup)** to collect related news content  
- **Transformer-based Sentence Embeddings** for semantic understanding  
- **Cosine Similarity Scoring** to measure caption–image alignment  
- **Gemini 2.5 Flash LLM Integration** for detailed misinformation reporting  
- **SQLite Database** for persistent hashing, scraped text, similarity scores, and reports  
- **Minimal Web Interface** for easy user interaction  

---

## 🛠️ Tech Stack

### Backend
- Python  
- Flask  
- Selenium  
- BeautifulSoup  
- Sentence Transformers  
- NumPy  
- OpenCV  
- SQLite  

### AI Components
- Sentence embedding model (MiniLM or equivalent)  
- Cosine similarity analysis  
- Gemini 2.5 Flash API  

### Frontend
- HTML  
- CSS  
- JavaScript  

---

## 🚀 How TrueTrace Works

1. **User Uploads Image + Caption**  
   From the web interface.

2. **Image is Converted into a Perceptual Hash (pHash)**  
   Used to detect duplicates and retrieve stored results.

3. **Web Scraping**  
   Selenium + BeautifulSoup gather related news captions from online sources.

4. **Embedding Generation**  
   The user caption and scraped captions are converted to sentence embeddings using a transformer model.

5. **Cosine Similarity Calculation**  
   Measures semantic similarity between captions.

6. **LLM Analysis (Gemini 2.5 Flash)**  
   The sentences and similarity scores are passed to an LLM to produce a detailed, human-readable report.

7. **Results Stored in SQLite**  
   Hash, scraped text.

8. **Frontend Displays**  
   - Similarity percentage  
   - Matched/mismatched captions  
   - Detailed misinformation analysis  

---

## 📊 Output Includes
- Similarity score (%)  
- Scraped captions  
- Semantic comparison results  
- LLM-generated misinformation explanation

---

## 🔍 Use Cases
- Verifying suspicious social-media posts  
- Checking whether an image is taken out of context  
- Supporting journalism and fact-checking workflows  
- Assisting researchers studying misinformation  
- Helping general users make informed decisions online  

---

## 🧩 Future Scope
- Support for multilingual captions and scraping  
- Browser extension for real-time verification  
- Mobile app version  
- Multimodal vision-language models (CLIP, BLIP, etc.)  
- Source credibility scoring  
- Manipulated/deepfake image detection  
- Cloud deployment and public API  
