from typing import List
import numpy as np 
from sentence_transformers import SentenceTransformer as st
from dotenv import load_dotenv
import os
from google import genai


load_dotenv()
llmKey = os.getenv("LLM_Key")
client = genai.Client(api_key=llmKey)


def getSimilarity(sentences: List[str]):
    try:
        model = st("all-MiniLM-L6-v2")
    except Exception as e:
        raise RuntimeError(
            "Could not load model."
        ) from e
    embeddings = model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms==0] = 1.0
    embeddings = embeddings/norms

    cosine = np.dot(embeddings[0], embeddings[1])

    percent = (cosine+1)/2*100

    return percent


def getReport(sentences):
    similarity = getSimilarity(sentences)
    prompt = f"""
                Compare the meaning of the following two news article captions and write a short report.
                Article 1: "{sentences[0]}"
                Article 2: "{sentences[1]}"
                First one is the actual news article and the second one is the one that we need to verify
                Similarity score: {similarity:.4f}
                Explain:
                1. What meanings are similar?
                2. What meanings are different?
                3. Are they paraphrases of each other?
                4. Are the words twisted to change the meaning?
                Don't give me any extra replies like Here's your caption and all. Just do the work...
                All I need is 2-3 lines and that's all.. Include all the points in those lines
                Dont refer to them as article 1 or 2. Refer the first article as "submitted article" and the second as article present in database
            """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    report = response.text
    return [similarity, report]