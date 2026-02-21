import json
import math
import requests
from pathlib import Path

EMBED_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb + 1e-9)

def gerar_embedding(texto):
    r = requests.post(EMBED_URL, json={
        "model": MODEL,
        "prompt": texto
    })
    r.raise_for_status()
    return r.json()["embedding"]

def buscar_blocos(pergunta, top_k=3):
    base = json.loads(
        Path("data/embeddings.json").read_text(encoding="utf-8")
    )

    emb_pergunta = gerar_embedding(pergunta)

    scores = []
    for item in base:
        sim = cosine_similarity(emb_pergunta, item["embedding"])
        scores.append((sim, item["text"]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [texto for _, texto in scores[:top_k]]
