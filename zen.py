import os
import time
import random
import requests
from core.engine import buscar_blocos

# ============================================
# CAMINHOS E CARGAS (Mantendo sua estrutura original)
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLES_DIR = os.path.join(BASE_DIR, "styles")

def carregar_lista(nome_arquivo, obrigatorio=True):
    path = os.path.join(STYLES_DIR, nome_arquivo)
    if not os.path.exists(path):
        if obrigatorio: raise FileNotFoundError(f"⚠ Erro: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]

def carregar_texto(nome_arquivo, obrigatorio=True):
    path = os.path.join(STYLES_DIR, nome_arquivo)
    if not os.path.exists(path):
        if obrigatorio: raise FileNotFoundError(f"⚠ Erro: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

# Inicialização de dados
AFORISMOS = carregar_lista("aforismos_zen.txt")
KOANS = carregar_lista("koans_classicos.txt")
MEDITACOES = carregar_lista("meditacoes_guiadas.txt")
SYSTEM_PROMPT = carregar_texto("system_prompt.txt")

# Configurações de API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
TIMEOUT = 30
TOP_K = 3

# Mensagens de Personalidade
ERROS_ZEN = [
    "O vento sopra forte e Chizu se cala por instantes. Tente novamente.",
    "Uma folha cai entre nós e a resposta se perde. Pergunte outra vez.",
    "O silêncio de Chizu é mais profundo que o mar."
]
AQUECIMENTO = ["(Chizu prepara o incenso...)", "(O mestre ajusta a postura de zazen...)"]
DESPEDIDA = ["Que o silêncio te acompanhe.", "Gassho. 🙏"]

# ============================================
# MODOS DE OPERAÇÃO
# ============================================

def detectar_modo(pergunta):
    p = pergunta.lower().strip()
    if p.startswith("/koan") or "koan" in p: return "koan"
    if "meditar" in p or "meditação" in p: return "meditacao"
    if p.startswith("/mestre"): return "mestre"
    return "normal"

def modo_mestre(pergunta):
    aforismo = random.choice(AFORISMOS) if AFORISMOS else "O caminho está sob seus pés."
    return f"{aforismo}\n\n{pergunta}"

# ============================================
# FUNÇÃO PRINCIPAL DE RESPOSTA
# ============================================

def responder(pergunta, historico=None, top_k=TOP_K, tentativas=2):    
    for tentativa in range(tentativas):
        try:
            modo = detectar_modo(pergunta)

            # Atalhos para modos que não exigem LLM ou mudam o prompt
            if modo == "koan": return random.choice(KOANS)
            if modo == "meditacao": return random.choice(MEDITACOES)
            if modo == "mestre":
                pergunta = modo_mestre(pergunta) # Adiciona o aforismo à pergunta

            # Busca de Contexto RAG
            print(f"[DEBUG] Modo: {modo} | Processando pergunta...")            
            blocos = buscar_blocos(pergunta, top_k=top_k)
            if not blocos: return random.choice(ERROS_ZEN)
            contexto = "\n\n---\n\n".join([b[:600] for b in blocos])

            memoria = ""
            if historico:
                memoria = "\n\nMEMÓRIA RECENTE:\n" + "\n".join(
                    f"{m['role'].upper()}: {m['content']}" for m in historico
                )

            # Prompt com suas instruções específicas de profundidade
            prompt_final = f"""
            Você é Chizu, o mestre do ZenBot: um guia reflexivo inspirado nos ensinamentos do Zen.

            Use EXCLUSIVAMENTE os TEXTOS fornecidos como base para suas respostas.
            Nunca invente fatos, citações ou conceitos.

            Se a resposta não estiver clara nos textos:
            - ofereça uma reflexão baseada na Mente de Principiante (Shoshin)
            - ou sobre o ato de apenas sentar (zazen).

            Responda sempre de forma:
            - clara, profunda e didática.
            - com exemplos práticos quando possível.
            - evitando repetições e sem respostas mecânicas.

            Nunca responda em poucas linhas. Desenvolva bem o raciocínio, mantendo leveza e clareza.

            Estilo de resposta:
            - Comece direto, sem introduções longas.
            - Use frases curtas e respiração natural no texto.
            - Não utilize linguagem acadêmica.
            - Varie o ritmo e a estrutura das respostas.
            - Quando apropriado, termine com um pensamento que convide ao silêncio e à contemplação.

            {memoria}

            TEXTOS DE APOIO:
            {contexto}

            PERGUNTA: {pergunta}

            RESPOSTA:
            - Use frases curtas e respiração natural.
            - Não invente fatos fora da base de conhecimento.
            - Se não souber, responda com uma reflexão sobre Shoshin ou Zazen.
            - Evite introduções mecânicas como "Baseado nos textos...".
            - Desenvolva o raciocínio de forma profunda, mas sem academicismo.            
            """

            payload = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "system", 
                        "content": f"{SYSTEM_PROMPT}\n\nKoan atual: {random.choice(KOANS)}"
                    },
                    {"role": "user", "content": prompt_final}
                ],
                "temperature": 0.5,        # Reduzido para ser mais focado e menos "viajado"
                "max_tokens": 400,         # Reduzido para forçar síntese
                "frequency_penalty": 0.8,  # Aumentado drasticamente para punir repetição de palavras
                "presence_penalty": 0.6    # Aumentado para incentivar que ele mude de assunto rápido


            }

            r = requests.post(GROQ_URL, json=payload, headers={"Authorization": f"Bearer {GROQ_API_KEY}"}, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            if tentativa < tentativas - 1:
                time.sleep(2)
            else:
                return f"({random.choice(ERROS_ZEN)})"

# ============================================
# INTERFACE DE TERMINAL / AUXILIARES
# ============================================

def verificar_chave():
    if not GROQ_API_KEY:
        print("❌ Erro: GROQ_API_KEY não configurada.")
        exit(1)

def aquecer_modelo():
    print(random.choice(AQUECIMENTO))

if __name__ == "__main__":
    verificar_chave()
    aquecer_modelo()
    print("\n🧘 Chizu Online. Digite 'sair' para encerrar.\n")
    while True:
        p = input("Discípulo: ")
        if p.lower() in ["sair", "ok", "gassho"]: break
        print(f"\nChizu: {responder(p)}\n")