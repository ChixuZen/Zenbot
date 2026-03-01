from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random
import json
import base64
import os
from zen import responder, verificar_chave, aquecer_modelo
from uuid import uuid4

AVATAR_B64 = ""
if os.path.exists("avatar.png"):
    with open("avatar.png", "rb") as img_file:
        AVATAR_B64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"

# Memória temporária em RAM (limpa quando o Render reinicia)
conversation_memory = {}

# ============================================
# INICIALIZAÇÃO
# ============================================
verificar_chave()
aquecer_modelo()
app = FastAPI()

# ============================================
# MENSAGENS ZEN PARA O FRONTEND
# ============================================
DESPEDIDA_JS = [
    "Que o silêncio te acompanhe.",
    "O caminho se abre diante de ti.",
    "Vá em paz. O vazio te espera.",
    "Que a mente de principiante floresça.",
    "Até o próximo encontro no vazio.",
    "O vento leva minhas palavras. Fica com o silêncio.",
    "Lembre-se: a montanha também é caminho."
]

AGUARDANDO_JS = [
    "Chizu medita...",
    "O mestre contempla sua pergunta...",
    "Uma brisa suave anuncia a resposta...",
    "O silêncio se aprofunda...",
    "Chizu respira fundo...",
    "As folhas balançam ao vento..."
]

# ============================================
# PÁGINA HTML COMPLETA (LAYOUT PREMIUM)
# ============================================
HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chizu · Mestre Zen</title>
    <style>
        body {{
            background: #f4f1ea;
            font-family: 'Georgia', serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 1rem;
            color: #2c3e2f;
        }}
        .container {{
            max-width: 550px;
            width: 100%;
            background: white;
            border-radius: 45px;
            padding: 4rem 2.5rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
            border: 1px solid #e0d6cc;
        }}
        h1 {{
            font-size: 2.8rem;
            margin: 0;
            font-weight: 400;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }}
        .sub {{
            font-size: 1.1rem;
            color: #4a5a4d;
            font-style: italic;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }}
        .ref {{
            font-size: 0.9rem;
            color: #8c8375;
            line-height: 1.4;
            margin-bottom: 3rem;
        }}
        .ref em {{
            color: #6b5e4a;
            font-style: italic;
            display: block;
            margin: 4px 0;
        }}

        input:focus {{
            border-color: #9b8c7c;
        }}

        .input-container {{ 
            margin-bottom: 1rem;
        }}

        input {{ 
            width: 100%; /* Faz o campo ocupar a largura total */
            box-sizing: border-box;
            padding: 1.2rem 1.6rem;
            border: 1px solid #e0d6cc;
            border-radius: 25px;
            font-family: inherit;
            font-size: 1.1rem;
            outline: none;
        }}

        .button-container {{ 
            margin: 1.5rem 0; /* Cria o espaço entre a pergunta e a resposta */
            text-align: center;
        }}

        button {{ 
            background: #2d362e;
            color: white;
            border: none;
            padding: 0.8rem 2.5rem; /* Ajustei o padding para um formato de botão melhor */
            border-radius: 25px;
            cursor: pointer;
            font-family: inherit;
            font-size: 1.1rem;
        }}


        button:hover {{
            background: #1f2620;
        }}
        button:disabled, input:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .loading {{
            opacity: 0.5;
            pointer-events: none;
        }}
        .resposta {{
            margin-top: 1rem;
            padding: 2rem;
            min-height: 120px;
            border: 1px solid #ede4db;
            border-radius: 30px;
            background: #fdfcfb;
            text-align: left;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #3e4a3f;
            white-space: pre-wrap;
        }}
        .resposta em {{
            color: #7f6e5d;
            font-style: italic;
        }}
        .avatar {{
            width: 120px; /* Tamanho ideal para o topo */
            height: auto;
            margin: 0 auto 1.5rem auto; /* Centraliza e dá espaço para o texto */
            display: block; /* Garante que o margin auto funcione */
        }}        
        .footer {{
            margin-top: 2.5rem;
            font-size: 0.85rem;
            color: #a3998e;
            letter-spacing: 0.5px;
        }}
        .doc-link {{
            display: block;
            margin-top: 10px;
            color: #8c8375;
            text-decoration: none;
            font-size: 0.8rem;
            transition: color 0.3s;
        }}
        .doc-link:hover {{
            color: #2d362e;
            text-decoration: underline;
        }}        
    </style>
</head>
<body>
    <div class="container">
        <h1>Chizu</h1>
        <div class="sub">mestre zen digital</div>
        <img src="{AVATAR_B64}" alt="Mestre Chizu" class="avatar">
        <div class="ref">
            Inspirado em<br>
            <em>"Mente Zen, Mente de Principiante"</em>
            Shunryu Suzuki
        </div>

        <!-- Pergunta -->
        <div class="input-container">
            <input type="text" id="pergunta" placeholder="Fale com Chizu" autofocus>
        </div>

        <!-- Botão entre a pergunta e a resposta -->
        <div class="button-container">
            <button id="perguntar">Enviar</button>
        </div>

        <!-- Resposta -->
        <div class="resposta" id="resposta">
            <em>O silêncio precede a resposta...</em>
        </div>

        <div class="footer">
            digite "sair", "ok" ou "gassho" para encerrar
            <a href="https://chizuzen.github.io/Zenbot/" target="_blank" class="doc-link">📖 Ver Documentação do Projeto</a>
        </div>

    </div>

    <script>
        const DESPEDIDA = {json.dumps(DESPEDIDA_JS)};
        const AGUARDANDO = {json.dumps(AGUARDANDO_JS)};
        const PALAVRAS_SAIDA = ['sair', 'exit', 'quit', 'gassho', 'obrigado'];

        const input = document.getElementById('pergunta');
        const button = document.getElementById('perguntar');
        const respostaDiv = document.getElementById('resposta');

        function randomMsg(arr) {{
            return arr[Math.floor(Math.random() * arr.length)];
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;
        }});

        async function fazerPergunta() {{
            const pergunta = input.value.trim();
            if (!pergunta) return;

            if (PALAVRAS_SAIDA.includes(pergunta.toLowerCase())) {{
                respostaDiv.innerHTML = `🧘 ${{randomMsg(DESPEDIDA)}}`;
                input.disabled = true;
                button.disabled = true;
                return;
            }}

            button.classList.add('loading');
            button.disabled = true;
            respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;

            try {{
                const response = await fetch('/ask', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ pergunta }})
                }});
                const data = await response.json();
                respostaDiv.innerHTML = data.resposta;
            }} catch (error) {{
                respostaDiv.innerHTML = '<em>(o vento levou sua pergunta...)</em>';
            }} finally {{
                button.classList.remove('loading');
                button.disabled = false;
            }}
            input.value = '';
        }}

        button.addEventListener('click', fazerPergunta);
        input.addEventListener('keypress', (e) => {{ if (e.key === 'Enter') fazerPergunta(); }});
    </script>
</body>
</html>
"""

# ============================================
# ROTAS DA API
# ============================================
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTML_PAGE

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
    except:
        return JSONResponse({"resposta": "(silêncio)"})

    pergunta = data.get("pergunta", "").strip()
    if not pergunta:
        return JSONResponse({"resposta": "(silêncio)"})

    if pergunta.lower() in {"sair", "exit", "quit", "gassho", "obrigado"}:
        return JSONResponse({"resposta": random.choice(DESPEDIDA_JS)})

    # Identificação da sessão para memória
    session_id = request.cookies.get("chizu_session") or str(uuid4())
    historico = conversation_memory.setdefault(session_id, [])

    # Chama o zen.py (certifique-se que responder aceita pergunta e historico)
    try:
        resposta = responder(pergunta, historico)
    except TypeError:
        # Fallback caso seu zen.py ainda não aceite histórico
        resposta = responder(pergunta)

    # Atualiza memória
    historico.append({"role": "user", "content": pergunta})
    historico.append({"role": "assistant", "content": resposta})
    conversation_memory[session_id] = historico[-6:]

    response = JSONResponse({"resposta": resposta})
    response.set_cookie("chizu_session", session_id, max_age=60*60*24*7)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)