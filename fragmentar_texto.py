from pathlib import Path

TXT_PATH = Path("textos/mente_zen_limpo.txt")
OUT_PATH = Path("textos/chunks.txt")

def main():
    texto = TXT_PATH.read_text(encoding="utf-8")

    paragrafos = [p.strip() for p in texto.split("\n\n") if len(p.strip()) > 200]

    print("Total de blocos:", len(paragrafos))

    OUT_PATH.write_text("\n\n---\n\n".join(paragrafos), encoding="utf-8")
    print("Chunks salvos em:", OUT_PATH)

if __name__ == "__main__":
    main()
