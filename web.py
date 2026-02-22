from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random
import json

app = FastAPI()

# ============================================
# DADOS DE TESTE (MOCK)
# ============================================
RESPOSTAS_ZEN = [
    "A resposta que você busca está no silêncio entre seus pensamentos.",
    "O rio não corre para o mar, ele se torna o mar.",
    "Não busque o caminho, o caminho é o agora.",
    "Uma xícara cheia não pode receber chá novo. Esvazie-se."
]

DESPEDIDA_JS = ["Que o silêncio te acompanhe.", "Gassho. 🙏"]
AGUARDANDO_JS = ["Chizu medita...", "O silêncio se aprofunda..."]

# ============================================
# PÁGINA HTML (Simplificada para o Teste)
# ============================================
HTML_PAGE = f"""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chizu · Mestre Zen (MODO TESTE)</title>
    <style>
        body {{ background: #f4f1ea; font-family: 'Georgia', serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
        .container {{ max-width: 500px; width: 90%; background: white; border-radius: 24px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e0d6cc; }}
        h1 {{ color: #2c3e2f; font-weight: 400; }}
        input {{ width: 80%; padding: 1rem; border-radius: 40px; border: 1px solid #e0d6cc; margin-bottom: 1rem; }}
        button {{ background: #2c3e2f; color: white; border: none; padding: 1rem 2rem; border-radius: 40px; cursor: pointer; }}
        .resposta {{ margin-top: 2rem; font-style: italic; color: #555; min-height: 50px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧘 Chizu</h1>
        <p>Modo de Teste de Infraestrutura Ativo</p>
        <input type="text" id="pergunta" placeholder="Faça uma pergunta...">
        <br>
        <button onclick="fazerPergunta()">Consultar Mestre</button>
        <div class="resposta" id="resposta">O mestre aguarda em silêncio...</div>
    </div>

    <script>
        async function fazerPergunta() {{
            const pergunta = document.getElementById('pergunta').value;
            const resDiv = document.getElementById('resposta');
            resDiv.innerText = "Chizu está contemplando...";
            
            const response = await fetch('/ask', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ pergunta }})
            }});
            const data = await response.json();
            resDiv.innerText = data.resposta;
        }}
    </script>
</body>
</html>
"""

# ============================================
# ROTAS
# ============================================
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTML_PAGE

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    # Simula uma resposta sem precisar do arquivo zen.py
    resposta = random.choice(RESPOSTAS_ZEN)
    return JSONResponse({"resposta": resposta})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)