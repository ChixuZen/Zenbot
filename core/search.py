import json
import math
import requests
from pathlib import Path

EMBED_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

# Cache global para armazenar os embeddings após primeira leitura
# Cache global para embeddings
_embeddings_cache = None

def carregar_embeddings():
    global _embeddings_cache
    if _embeddings_cache is None:
        caminho = Path("data/embeddings_bge.json")
        if not caminho.exists():
            raise FileNotFoundError("Arquivo data/embeddings_bge.json não encontrado.")
        with open(caminho, "r", encoding="utf-8") as f:
            _embeddings_cache = json.load(f)
    return _embeddings_cache



def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb + 1e-9)

def gerar_embedding(texto):
    payload = {
        "model": MODEL,
        "input": texto
    }
    try:
        print(f"[DEBUG] Enviando requisição para {EMBED_URL} com payload: {payload}")
        r = requests.post(EMBED_URL, json=payload, timeout=30)
        print(f"[DEBUG] Status code: {r.status_code}")
        print(f"[DEBUG] Resposta bruta: {r.text[:500]}")  # primeiros 500 caracteres
        r.raise_for_status()
        data = r.json()
        print(f"[DEBUG] JSON decodificado: {data}")
        # A API retorna {"data": [{"embedding": [...]}]}
        return data["data"][0]["embedding"]
    except Exception as e:
        print(f"[DEBUG] Exceção: {e}")
        raise

def buscar_blocos(pergunta, top_k=3):
    base = carregar_embeddings()
    emb_pergunta = gerar_embedding(pergunta)

    scores = []
    for item in base:
        sim = cosine_similarity(emb_pergunta, item["embedding"])
        scores.append((sim, item["texto"]))
        print(f"[DEBUG] Similaridade com bloco {item['id']}: {sim:.4f}")   # <--- TEM QUE APARECER

    scores.sort(reverse=True, key=lambda x: x[0])
    print(f"[DEBUG] Maior similaridade: {scores[0][0]:.4f} (threshold={THRESHOLD})")

    if not scores or scores[0][0] < THRESHOLD:
        print("[DEBUG] Nenhum bloco atingiu o limiar. Usando resposta zen.")
        return [random.choice(RESPOSTAS_ZEN)]

    selecionados = [texto for _, texto in scores[:top_k]]
    print(f"[DEBUG] {len(selecionados)} blocos selecionados.")
    return selecionados