import json
import time
from pathlib import Path
from core.engine import gerar_embedding

# Configurações
CHUNKS_PATH = Path("textos/chunks.txt")
OUTPUT_PATH = Path("data/embeddings_bge.json")
PAUSA_PADRAO = 6  # segundos entre requisições (respeita 10/min)
PAUSA_429 = 60    # segundos para esperar quando atingir rate limit

def carregar_embeddings_existentes():
    """Carrega embeddings já salvos, se existirem."""
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def main():
    # Carrega blocos originais
    if not CHUNKS_PATH.exists():
        print(f"❌ Arquivo {CHUNKS_PATH} não encontrado.")
        return

    blocos_raw = CHUNKS_PATH.read_text(encoding="utf-8").split("\n\n---\n\n")
    blocos = [b.strip() for b in blocos_raw if b.strip()]
    total = len(blocos)
    print(f"✅ Total de blocos: {total}")

    # Carrega embeddings já processados
    embeddings_existentes = carregar_embeddings_existentes()
    ids_processados = {item["id"] for item in embeddings_existentes}
    print(f"📂 Embeddings já processados: {len(ids_processados)} blocos")

    novos_embeddings = []

    for i, bloco in enumerate(blocos, start=1):
        if i in ids_processados:
            print(f"⏩ Bloco {i}/{total} já processado. Pulando.")
            continue

        print(f"⏳ Gerando embedding {i}/{total}...")

        # Trunca se necessário
        if len(bloco) > 4000:
            bloco = bloco[:4000]

        # Tenta com retry em caso de 429
        tentativas = 0
        while True:
            try:
                vec = gerar_embedding(bloco)
                break  # sucesso
            except Exception as e:
                if "429" in str(e):
                    tentativas += 1
                    print(f"⚠️ Rate limit atingido. Aguardando {PAUSA_429}s... (tentativa {tentativas})")
                    time.sleep(PAUSA_429)
                else:
                    print(f"❌ Erro no bloco {i}: {e}")
                    # Se for outro erro, aborta ou pode pular
                    raise  # ou continue, dependendo da gravidade

        # Salva o embedding
        novos_embeddings.append({
            "id": i,
            "texto": bloco,
            "embedding": vec
        })

        # Aguarda antes da próxima requisição
        if i < total:  # não espera após o último
            time.sleep(PAUSA_PADRAO)

    # Combina existentes + novos e salva
    todos_embeddings = embeddings_existentes + novos_embeddings
    # Ordena por id para manter consistência
    todos_embeddings.sort(key=lambda x: x["id"])

    OUTPUT_PATH.write_text(json.dumps(todos_embeddings, ensure_ascii=False, indent=2))
    print(f"✅ Embeddings salvos em {OUTPUT_PATH} com {len(todos_embeddings)} blocos.")

if __name__ == "__main__":
    main()