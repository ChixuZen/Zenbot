import json
import math
import random
import requests
from pathlib import Path

# Endpoint do Ollama para embeddings
EMBED_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

# Limiar de similaridade (threshold) para aceitar respostas relevantes:
#
# 0.30 → muito permissivo (quase tudo passa, mais ruído)
# 0.40 → equilibrado
# 0.45 → bom padrão (recomendado)
# 0.50 → rigoroso (mais precisão, menos cobertura)
# 0.60 → extremamente seletivo (só respostas muito próximas)
#
# Ajuste conforme o comportamento desejado do Chizu:
# mais contemplativo → valores menores
# mais preciso       → valores maiores

# Limiar mínimo de similaridade para aceitar uma resposta
THRESHOLD = 0.45

# Respostas contemplativas quando não há boa correspondência
RESPOSTAS_ZEN = [
    "A resposta não está nas palavras, mas no silêncio entre elas.",
    "A mente que pergunta já contém a resposta.",
    "Quando nada surge, o vazio se revela.",
    "Talvez não haja nada a buscar.",
    "Observe este instante antes de perguntar novamente.",
    "O caminho não se revela ao ser forçado.",
    "A pergunta correta dissolve a necessidade da resposta."
]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-9)


def gerar_embedding(texto):
    r = requests.post(
        EMBED_URL,
        json={
            "model": MODEL,
            "prompt": texto
        },
        timeout=60
    )
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

    melhor_score = scores[0][0]

    if melhor_score < THRESHOLD:
        return [random.choice(RESPOSTAS_ZEN)]

    return [texto for _, texto in scores[:top_k]]