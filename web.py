from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random
import json
from zen import responder, verificar_chave, aquecer_modelo
from uuid import uuid4

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
# PÁGINA HTML
# ============================================
HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chizu · Mestre Zen</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    background: linear-gradient(180deg,#f4f1ea,#ebe6dc);
    font-family: 'Inter', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 1rem;
}}

.container {{
    width: 100%;
    max-width: 720px;
    background: #fffdf9;
    border-radius: 28px;
    padding: 3rem 2.5rem;
    box-shadow: 0 25px 50px rgba(0,0,0,.08);
    border: 1px solid #e6ded3;
}}

header {{ text-align: center; margin-bottom: 2.5rem; }}

h1 {{
    font-family: 'Playfair Display', serif;
    font-weight: 500;
    margin: 0;
    font-size: 2.6rem;
    color: #2c3e2f;
}}

.sub {{
    margin-top: .5rem;
    font-style: italic;
    color: #6f6455;
}}

.ref {{
    margin-top: 1.2rem;
    font-size: .9rem;
    color: #9b8f7d;
}}

.input-group {{
    display: flex;
    gap: .8rem;
    margin-top: 2rem;
}}

input {{
    flex: 1;
    padding: 1.1rem 1.4rem;
    border-radius: 40px;
    border: 1.8px solid #d8cfc3;
    background: #fefcf8;
    font-size: 1rem;
}}

input:focus {{ outline: none; border-color: #9b8c7c; }}

button {{
    border-radius: 40px;
    border: none;
    padding: 1.1rem 2.4rem;
    background: linear-gradient(135deg,#2c3e2f,#1f2e22);
    color: white;
    font-size: 1rem;
    cursor: pointer;
}}

button:hover {{ filter: brightness(1.05); }}

.resposta {{
    margin-top: 2.2rem;
    padding: 1.8rem 1.8rem;
    border-radius: 22px;
    background: #fefcf8;
    border: 1px solid #e6ded3;
    font-size: 1.15rem;
    line-height: 1.65;
    color: #2c3e2f;
    min-height: 130px;
}}

.resposta em {{ color: #7f6e5d; font-style: italic; }}

.footer {{
    margin-top: 2.4rem;
    text-align: center;
    font-size: .8rem;
    color: #b2a392;
}}

@media (max-width: 600px) {{
    .container {{ padding: 2.2rem 1.6rem; }}
    h1 {{ font-size: 2.1rem; }}
}}
</style>
</head>
<body>

<div class="container">
<header>
<h1>🧘 Chizu</h1>
<div class="sub">Mestre Zen digital</div>
<div class="ref">Inspirado em<br><em>"Mente Zen, Mente de Principiante"</em><br>Shunryu Suzuki</div>
</header>

<div class="input-group">
<input id="pergunta" type="text" placeholder="sua pergunta..." autofocus>
<button id="perguntar">perguntar</button>
</div>

<div id="resposta" class="resposta"></div>

<div class="footer">digite "sair" ou "gassho" para encerrar</div>
</div>

<script>
const DESPEDIDA = {json.dumps(DESPEDIDA_JS)};
const AGUARDANDO = {json.dumps(AGUARDANDO_JS)};
const PALAVRAS_SAIDA = ['sair','exit','quit','gassho','obrigado'];

const input = document.getElementById('pergunta');
const button = document.getElementById('perguntar');
const respostaDiv = document.getElementById('resposta');

function randomMsg(arr) {{ return arr[Math.floor(Math.random()*arr.length)]; }}

respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;

async function fazerPergunta() {{
    const pergunta = input.value.trim();
    if (!pergunta) return;

    if (PALAVRAS_SAIDA.includes(pergunta.toLowerCase())) {{
        respostaDiv.innerHTML = `🧘 ${{randomMsg(DESPEDIDA)}}`;
        input.disabled = true;
        button.disabled = true;
        return;
    }}

    respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;

    try {{
        const response = await fetch('/ask', {{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body: JSON.stringify({{pergunta}})
        }});
        const data = await response.json();
        respostaDiv.innerHTML = data.resposta.replace(/\n/g,'<br>');
    }} catch {{
        respostaDiv.innerHTML = '<em>(o vento levou sua pergunta...)</em>';
    }}
    input.value='';
}}

button.onclick = fazerPergunta;
input.onkeypress = e => {{ if(e.key==='Enter') fazerPergunta(); }}
</script>
</body>
</html>
"""

# ============================================
# ROTAS
# ============================================
@app.get("/", response_class=HTMLResponse)
async def index():
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

    if pergunta.lower() in {"sair","exit","quit","gassho","obrigado"}:
        return JSONResponse({"resposta": random.choice(DESPEDIDA_JS)})

    session_id = request.cookies.get("chizu_session") or str(uuid4())
    historico = conversation_memory.setdefault(session_id, [])

    resposta = responder(pergunta, historico)

    historico.append({"role":"user","content":pergunta})
    historico.append({"role":"assistant","content":resposta})
    conversation_memory[session_id] = historico[-6:]

    response = JSONResponse({"resposta": resposta})
    response.set_cookie("chizu_session", session_id, max_age=60*60*24*7)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
