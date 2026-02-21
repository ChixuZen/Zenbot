import re
from pathlib import Path

TXT_PATH = Path("textos/mente_zen.txt")
OUT_PATH = Path("textos/mente_zen_limpo.txt")


def limpar(texto: str) -> str:
    # Remove cabeçalhos repetidos
    texto = re.sub(r"MENTE ZEN,\s*MENTE DE PRINCIPIANTE", "", texto, flags=re.I)

    # Remove números soltos de página
    texto = re.sub(r"\n\s*\d+\s*\n", "\n", texto)

    # Corrige quebras estranhas no meio de palavras
    texto = re.sub(r"-\n", "", texto)

    # Remove espaços excessivos
    texto = re.sub(r"[ \t]+", " ", texto)

    # Remove múltiplas quebras de linha
    texto = re.sub(r"\n{3,}", "\n\n", texto)

    return texto.strip()


def main():
    bruto = TXT_PATH.read_text(encoding="utf-8")
    limpo = limpar(bruto)
    OUT_PATH.write_text(limpo, encoding="utf-8")
    print("Texto limpo salvo em:", OUT_PATH)
    print("Tamanho final:", len(limpo) // 1024, "KB")


if __name__ == "__main__":
    main()
