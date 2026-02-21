import requests
import json
import time
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"

def gerar_embedding(texto, tentativas=3):
    payload = {
        "model": MODEL,
        "prompt": texto
    }

    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["embedding"]

        except Exception as e:
            print(f"⚠️ Erro na tentativa {tentativa}: {e}")
            time.sleep(2 * tentativa)

    raise RuntimeError("Falha ao gerar embedding após várias tentativas.")

def main():
    chunks_path = Path("textos/chunks.txt")
    out_path = Path("data/embeddings.json")

    blocos = chunks_path.read_text(encoding="utf-8").split("\n\n---\n\n")

    embeddings = []

    total = len(blocos)
    print(f"Total de blocos: {total}")

    for i, bloco in enumerate(blocos, 1):
        print(f"Gerando embedding {i}/{total}")

        bloco = bloco.strip()

        if not bloco:
            continue

        if len(bloco) > 4000:
            print("⚠️ Bloco muito grande — truncando")
            bloco = bloco[:4000]

        vec = gerar_embedding(bloco)

        embeddings.append({
            "id": i,
            "texto": bloco,
            "embedding": vec
        })

        time.sleep(0.3)  # proteção contra overload

    out_path.write_text(json.dumps(embeddings, ensure_ascii=False, indent=2))
    print("✅ Embeddings gerados com sucesso!")

if __name__ == "__main__":
    main()
