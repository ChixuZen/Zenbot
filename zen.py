import time
import random
import requests
from core.search import buscar_blocos

# ============================================
# CONFIGURAÇÕES
# ============================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"        # Modelo leve
TIMEOUT = 120
TOP_K = 5

# ============================================
# MENSAGENS ZEN RANDOMIZADAS
# ============================================

# Mensagens de erro (quando a IA falha após tentativas)
ERROS_ZEN = [
    "O vento sopra forte e Chizu se cala por instantes. Tente novamente.",
    "Uma folha cai entre nós e a resposta se perde. Pergunte outra vez.",
    "O silêncio de Chizu é mais profundo que o mar. Talvez mais tarde.",
    "A névoa escondeu o caminho. Faça sua pergunta novamente.",
    "O mestre cochilou por um instante. Perdoe‑o e repita.",
    "O eco demorou a voltar do vale. Tente agora.",
    "Chizu observa a lua e não ouve sua pergunta. Diga‑a de novo.",
    "Uma nuvem passageira encobriu a resposta. Aguarde e pergunte outra vez.",
    "O vento levou suas palavras. Fale mais alto? Brincadeira. Repita.",
    "O mestre está em meditação profunda. Aguarde um momento e tente de novo."
]

# Mensagens de aquecimento (warm-up)
AQUECIMENTO = [
    "(Aquecendo o mestre... aguarde)",
    "(Chizu prepara o incenso... só um instante)",
    "(O mestre ajusta a postura de zazen...)",
    "(Uma brisa suave anuncia a presença de Chizu...)",
    "(O silêncio se acomoda antes da fala...)",
    "(Chizu respira fundo e se prepara para ouvir...)"
]

# Mensagens de despedida
DESPEDIDA = [
    "Que o silêncio te acompanhe.",
    "O caminho se abre diante de ti.",
    "Vá em paz. O vazio te espera.",
    "Que a mente de principiante floresça.",
    "Até o próximo encontro no vazio.",
    "O vento leva minhas palavras. Fica com o silêncio.",
    "Lembre-se: a montanha também é caminho."
]

# Mensagens quando não há blocos (contexto vazio)
SEM_CONTEXTO = [
    "(Silêncio.)",
    "(O vazio responde por si.)",
    "(Nem uma folha se move.)",
    "(Chizu apenas sorri.)"
]

# Mensagens durante tentativa de retry
RETRY_MSG = [
    "(Chizu hesita... tentando novamente.)",
    "(O vento sopra e a resposta demora...)",
    "(Uma nuvem passa... mais um instante.)",
    "(O mestre respira fundo e repete o movimento.)",
    "(O eco ainda não voltou. Aguarde.)"
]

# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def verificar_ollama():
    try:
        requests.get("http://localhost:11434/api/tags", timeout=5)
    except:
        print("❌ Ollama não está acessível. Certifique-se de que está rodando (ollama serve).")
        exit(1)

def aquecer_modelo():
    print(random.choice(AQUECIMENTO))
    try:
        requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": "Olá", "stream": False}, timeout=60)
    except:
        pass

def responder(pergunta, top_k=TOP_K, tentativas=2):
    for tentativa in range(tentativas):
        try:
            blocos = buscar_blocos(pergunta, top_k=top_k)
            if not blocos:
                return random.choice(SEM_CONTEXTO)

            contexto = "\n\n".join(blocos)

            prompt = f"""
Você é Chizu, um mestre zen tradicional.
Fale pouco. Use frases curtas.
Não explique demais. Não dê conselhos diretos.
Se a pergunta for confusa, devolva a confusão.
Se for simples, responda com simplicidade.
Às vezes, responda com uma pergunta.
Seja paradoxal quando necessário.
Baseie-se apenas nos textos abaixo.

TEXTOS:
{contexto}

PERGUNTA:
{pergunta}

RESPOSTA:
"""
            r = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()["response"].strip()

        except requests.exceptions.Timeout:
            if tentativa < tentativas - 1:
                print(random.choice(RETRY_MSG))
                time.sleep(2)
            else:
                return f"({random.choice(ERROS_ZEN)})"

        except Exception as e:
            if tentativa < tentativas - 1:
                print(f"(Ocorreu um erro inesperado, mas Chizu persiste... tentativa {tentativa+2})")
                time.sleep(2)
            else:
                return f"({random.choice(ERROS_ZEN)})"

def main():
    verificar_ollama()
    aquecer_modelo()

    print("\n🧘‍♂️ Chizu — Mestre Zen Digital")
    print("Digite 'ok', 'sair', 'gassho' ou 'obrigado' para encerrar.\n")

    while True:
        pergunta = input("Discípulo: ").strip()
        if not pergunta:
            continue

        if pergunta.lower() in {"ok", "sair", "exit", "quit", "gassho", "obrigado"}:
            print(f"\nChizu: {random.choice(DESPEDIDA)}\n")
            break

        resposta = responder(pergunta)
        print(f"\nChizu: {resposta}\n")

if __name__ == "__main__":
    main()