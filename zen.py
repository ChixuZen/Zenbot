import os
import time
import random
import requests
from core.engine import buscar_blocos

# ============================================
# CAMINHOS BASE
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLES_DIR = os.path.join(BASE_DIR, "styles")

# ============================================
# FUNÇÕES DE CARGA
# ============================================

def escolha_segura(lista, fallback):
    return random.choice(lista) if lista else fallback

def carregar_lista(nome_arquivo, obrigatorio=True):
    path = os.path.join(STYLES_DIR, nome_arquivo)

    if not os.path.exists(path):
        msg = f"⚠ Arquivo não encontrado: {path}"
        if obrigatorio:
            raise FileNotFoundError(msg)
        print(msg)
        return []

    with open(path, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f.read().splitlines() if l.strip()]

    if obrigatorio and not linhas:
        raise ValueError(f"⚠ Arquivo vazio: {path}")

    return linhas


def carregar_texto(nome_arquivo, obrigatorio=True):
    path = os.path.join(STYLES_DIR, nome_arquivo)

    if not os.path.exists(path):
        msg = f"⚠ Arquivo não encontrado: {path}"
        if obrigatorio:
            raise FileNotFoundError(msg)
        print(msg)
        return ""

    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


# ============================================
# CARGA DOS ESTILOS ZEN
# ============================================

AFORISMOS = carregar_lista("aforismos_zen.txt")
KOANS_CLASSICOS = carregar_lista("koans_classicos.txt")
MEDITACOES = carregar_lista("meditacoes_guiadas.txt")

# Koan do momento usa os clássicos
KOANS = KOANS_CLASSICOS

SYSTEM_PROMPT = carregar_texto("system_prompt.txt")

# ============================================
# LOG DE INICIALIZAÇÃO
# ============================================

print("🧘 Estilos Zen carregados:")
print(f"   • Aforismos: {len(AFORISMOS)}")
print(f"   • Koans clássicos: {len(KOANS_CLASSICOS)}")
print(f"   • Meditações: {len(MEDITACOES)}")
    
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
# DETECÇÃO DE MODO
# ============================================

def detectar_modo(pergunta):
    p = pergunta.lower().strip()

    if p.startswith("/koan") or "koan" in p:
        return "koan"

    if p.startswith("/meditar") or "meditar" in p or "meditação" in p:
        return "meditacao"

    if p.startswith("/mestre"):
        return "mestre"

    return "normal"


# ============================================
# MODOS DE RESPOSTA
# ============================================
def modo_koan():
    return escolha_segura(
        KOANS_CLASSICOS,
        "Quando não há palavras, o silêncio responde."
    )


def modo_meditacao():
    return escolha_segura(
        MEDITACOES,
        "Sente-se. Respire. Apenas isso."
    )


def modo_mestre(pergunta):
    aforismo = escolha_segura(
        AFORISMOS,
        "O caminho não está fora."
    )
    return f"{aforismo}\n\n{pergunta}"



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

            modo = detectar_modo(pergunta)

            if modo == "koan":
                return modo_koan()

            if modo == "meditacao":
                return modo_meditacao()

            if modo == "mestre":
                pergunta = modo_mestre(pergunta)

            # Busca os blocos mais relevantes
            print("[DEBUG] Pergunta recebida:", pergunta)            
            blocos = buscar_blocos(pergunta, top_k=top_k)
            if not blocos:
                return random.choice(ERROS_ZEN)

            # Limita cada bloco para não estourar o contexto
            blocos_limitados = [b[:600] for b in blocos]
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
                        "content": f"""
                        {SYSTEM_PROMPT}
                        Koan do momento:
                        {random.choice(KOANS)}
                        """
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