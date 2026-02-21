import fitz  # pymupdf
import re
from unidecode import unidecode
from pathlib import Path

PDF_PATH = Path("textos/Mente_Zen_Mente_de_Principiante.pdf")
TXT_PATH = Path("textos/mente_zen.txt")


def limpar_texto(texto: str) -> str:
    texto = texto.replace("\r", "")
    texto = re.sub(r"-\n", "", texto)          # remove hifenização artificial
    texto = re.sub(r"\n{2,}", "\n\n", texto)   # normaliza parágrafos
    texto = re.sub(r"[ \t]+", " ", texto)      # espaços extras
    return texto.strip()


def extrair_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    texto = []
    for page in doc:
        texto.append(page.get_text())
    return "\n".join(texto)


def main():
    bruto = extrair_pdf(PDF_PATH)
    limpo = limpar_texto(bruto)

    TXT_PATH.write_text(limpo, encoding="utf-8")

    print(f"Texto extraído e salvo em: {TXT_PATH.resolve()}")


if __name__ == "__main__":
    main()
