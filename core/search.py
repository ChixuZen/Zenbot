import json
import math
import requests
from pathlib import Path

EMBED_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

# Cache global para armazenar os embeddings após primeira leitura
_embeddings_cache = None

def carregar_embeddings():
    """
    Carrega os embeddings do arquivo JSON uma única vez e os armazena em cache.
    Retorna a lista de itens (cada item contém 'id', 'texto', 'embedding').
    """
    global _embeddings_cache
    if _embeddings_cache is None:
        caminho = Path("data/embeddings.json")
        if not caminho.exists():
            raise FileNotFoundError("Arquivo data/embeddings.json não encontrado. Execute core/embeddings.py primeiro.")
        with open(caminho, "r", encoding="utf-8") as f:
            _embeddings_cache = json.load(f)
    return _embeddings_cache

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
    # Obtém a base de embeddings (agora em cache)
    base = carregar_embeddings()

    # Gera embedding para a pergunta do usuário
    emb_pergunta = gerar_embedding(pergunta)

    # Calcula similaridade com cada bloco
    scores = []
    for item in base:
        sim = cosine_similarity(emb_pergunta, item["embedding"])
        # Assume que a chave para o texto é "texto" (conforme gerado pelo embeddings.py)
        scores.append((sim, item["texto"]))

    # Ordena do mais similar para o menos similar
    scores.sort(reverse=True, key=lambda x: x[0])

    # Retorna apenas os textos dos top_k blocos
    return [texto for _, texto in scores[:top_k]]