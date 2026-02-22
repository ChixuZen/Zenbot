import os
import time
import random
import requests
from core.engine import buscar_blocos

# ============================================
# CONFIGURAÇÕES
# ============================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")          # Obrigatório
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
TIMEOUT = 30
TOP_K = 3

# ============================================
# MENSAGENS ZEN RANDOMIZADAS
# ============================================
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

AQUECIMENTO = [
    "(Aquecendo o mestre... aguarde)",
    "(Chizu prepara o incenso... só um instante)",
    "(O mestre ajusta a postura de zazen...)",
    "(Uma brisa suave anuncia a presença de Chizu...)",
    "(O silêncio se acomoda antes da fala...)",
    "(Chizu respira fundo e se prepara para ouvir...)"
]

DESPEDIDA = [
    "Que o silêncio te acompanhe.",
    "O caminho se abre diante de ti.",
    "Vá em paz. O vazio te espera.",
    "Que a mente de principiante floresça.",
    "Até o próximo encontro no vazio.",
    "O vento leva minhas palavras. Fica com o silêncio.",
    "Lembre-se: a montanha também é caminho."
]

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
def verificar_chave():
    """Verifica se a chave da API Groq está definida."""
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY não definida. Configure a variável de ambiente.")
        exit(1)

def aquecer_modelo():
    """Mensagem de aquecimento (não faz requisição real, apenas estética)."""
    print(random.choice(AQUECIMENTO))


def responder(pergunta, historico=None, top_k=TOP_K, tentativas=2):    
    """
    Envia a pergunta para a API Groq, com contexto dos textos zen.
    Em caso de falha, tenta novamente e, se tudo falhar, retorna uma mensagem zen aleatória.
    """
    for tentativa in range(tentativas):
        try:
            # Busca os blocos mais relevantes
            blocos = buscar_blocos(pergunta, top_k=top_k)
            if not blocos:
                return random.choice(ERROS_ZEN)

            # Limita cada bloco para não estourar o contexto
            blocos_limitados = [b[:700] for b in blocos]
            contexto = "\n\n---\n\n".join(blocos_limitados)
 

            memoria = ""
            if historico:
                memoria = "\n\nMEMÓRIA RECENTE:\n" + "\n".join(
                    f"{m['role'].upper()}: {m['content']}" for m in historico
                )

            prompt = f"""
            Instrução para Chizu:
            Use os TEXTOS abaixo como base para sua sabedoria. 
            Se a resposta não estiver clara nos textos, não tente inventar fatos; em vez disso, 
            ofereça uma reflexão sobre a Mente de Principiante ou sobre o ato de apenas sentar (zazen).

            Estilo de resposta:
            - Comece direto, sem introduções longas.
            - Use frases curtas. Se possível, termine com um pensamento que faça o discípulo silenciar.
            - Não use linguagem acadêmica.            

{memoria}

TEXTOS:
{contexto}

PERGUNTA: {pergunta}

RESPOSTA:
"""

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            "Você é o Mestre Zen Shunryu Suzuki (Chizu). Sua voz é gentil e direta. "
                            "Sua filosofia baseia-se na 'Mente de Principiante': simplicidade e presença. "
                            "Você não busca explicar conceitos complexos, mas sim trazer o discípulo para a realidade do agora. "
                            "Use metáforas da natureza (chuva, folhas, nuvens) e seja breve. "
                            "Mantenha um tom de não-dualidade, tratando tudo com aceitação."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.35,
                "max_tokens": 300
            }

            r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=TIMEOUT)
            print(f"[LOG] Status Groq: {r.status_code}")
            print(f"[LOG] Resposta bruta: {r.text[:200]}")
            r.raise_for_status()
            resposta = r.json()["choices"][0]["message"]["content"].strip()
            return resposta

        except Exception as e:
            print(f"\n[ERRO DETALHADO] {type(e).__name__}: {e}")
            if tentativa < tentativas - 1:
                print(f"(Ocorreu um erro inesperado, mas Chizu persiste... tentativa {tentativa+2})")
                time.sleep(2)
            else:
                return f"({random.choice(ERROS_ZEN)})"

def main():
    verificar_chave()
    aquecer_modelo()

    print("\n🧘‍♂️ Chizu — Mestre Zen Digital (via Groq)")
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