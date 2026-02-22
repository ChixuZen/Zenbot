import json
import math
import random
import requests
import os
from pathlib import Path

EMBED_URL = os.getenv("EMBED_URL", "http://localhost:11434/api/embeddings")
MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

# Limiar de similaridade (ajuste conforme necessário)
THRESHOLD = 0.20

# Respostas contemplativas quando não há boa correspondência
RESPOSTAS_ZEN = [
    "A resposta não está nas palavras, mas no silêncio entre elas.",
    "A mente que pergunta já contém a resposta.",
    "Quando nada surge, o vazio se revela.",
    "Talvez não haja nada a buscar.",
    "Observe este instante antes de perguntar novamente.",
    "O caminho não se revela ao ser forçado.",
    "A pergunta correta dissolve a necessidade da resposta.",
    "A resposta está no silêncio, não nas palavras.",
    "Observe sua própria mente enquanto pergunta.",
    "Talvez a pergunta seja mais importante que a resposta.",
    "O vento levou a resposta... tente novamente mais tarde.",
    "Não há palavras para isso, apenas prática."
]

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)

def gerar_embedding(texto):
    payload = {
        "model": MODEL,
        "input": texto
    }
    try:
        r = requests.post(EMBED_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["data"][0]["embedding"]
    except Exception as e:
        # Log crítico (opcional, pode ser removido)
        # print(f"[ERRO] gerar_embedding: {e}")
        raise

def buscar_blocos(pergunta, top_k=3):
    # Carrega os embeddings do arquivo (certifique-se de que o caminho está correto)
    with open("data/embeddings_bge.json", "r", encoding="utf-8") as f:
        base = json.load(f)

    emb_pergunta = gerar_embedding(pergunta)

    scores = []
    for item in base:
        sim = cosine_similarity(emb_pergunta, item["embedding"])
        scores.append((sim, item["texto"]))

    scores.sort(reverse=True, key=lambda x: x[0])

    if not scores or scores[0][0] < THRESHOLD:
        return [random.choice(RESPOSTAS_ZEN)]

    return [texto for _, texto in scores[:top_k]]