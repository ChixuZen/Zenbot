from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import random
import json

# Importa do zen.py tudo o que precisamos
from zen import responder, verificar_ollama, aquecer_modelo

# Executa verificações e aquecimento assim que o servidor iniciar
verificar_ollama()
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
    "As folhas balançam ao vento...",
    "O incenso queima lentamente...",
    "A névoa se dissipa...",
    "O vento carrega as palavras..."
]

# ============================================
# PÁGINA HTML (com CSS e JavaScript embutidos)
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
        }}
        .container {{
            max-width: 600px;
            width: 100%;
            background: white;
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            border: 1px solid #e0d6cc;
        }}
        h1 {{
            font-size: 2rem;
            font-weight: 400;
            color: #2c3e2f;
            margin-top: 0;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }}
        .sub {{
            color: #6b5e4a;
            font-style: italic;
            margin-bottom: 2rem;
            border-bottom: 1px dashed #dcd3c9;
            padding-bottom: 1rem;
        }}
        .input-group {{
            display: flex;
            gap: 0.5rem;
        }}
        input {{
            flex: 1;
            padding: 1rem;
            border: 2px solid #e0d6cc;
            border-radius: 40px;
            font-size: 1rem;
            font-family: inherit;
            background: #fefcf8;
            transition: border 0.2s;
        }}
        input:focus {{
            outline: none;
            border-color: #9b8c7c;
        }}
        button {{
            background: #2c3e2f;
            color: white;
            border: none;
            border-radius: 40px;
            padding: 1rem 2rem;
            font-size: 1rem;
            cursor: pointer;
            font-family: inherit;
            transition: background 0.2s;
        }}
        button:hover {{
            background: #1f2e22;
        }}
        button:disabled, input:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .resposta {{
            margin-top: 2rem;
            padding: 1.5rem;
            background: #fefcf8;
            border-radius: 20px;
            border: 1px solid #e0d6cc;
            min-height: 100px;
            white-space: pre-wrap;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #2c3e2f;
        }}
        .resposta em {{
            color: #7f6e5d;
            font-style: italic;
        }}
        .footer {{
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #b2a392;
            text-align: center;
        }}
        .loading {{
            opacity: 0.5;
            pointer-events: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧘 Chizu</h1>
        <div class="sub">mestre zen digital</div>

        <div class="input-group">
            <input type="text" id="pergunta" placeholder="sua pergunta..." autofocus>
            <button id="perguntar">perguntar</button>
        </div>

        <div class="resposta" id="resposta">
            <!-- A mensagem inicial será inserida dinamicamente pelo JavaScript -->
        </div>

        <div class="footer">
            para encerrar, digite "sair", "gassho" ou "obrigado"
        </div>
    </div>

    <script>
        // ============================================
        // MENSAGENS ZEN RANDOMIZADAS
        // ============================================
        const DESPEDIDA = {json.dumps(DESPEDIDA_JS)};
        const AGUARDANDO = {json.dumps(AGUARDANDO_JS)};

        // Palavras que encerram a conversa
        const PALAVRAS_SAIDA = ['sair', 'exit', 'quit', 'gassho', 'obrigado'];

        // Elementos da página
        const input = document.getElementById('pergunta');
        const button = document.getElementById('perguntar');
        const respostaDiv = document.getElementById('resposta');

        // Função para escolher uma mensagem aleatória de um array
        function randomMsg(arr) {{
            return arr[Math.floor(Math.random() * arr.length)];
        }}

        // Define uma mensagem inicial aleatória ao carregar a página
        window.addEventListener('DOMContentLoaded', () => {{
            respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;
        }});

        // Função para encerrar a conversa
        function encerrarConversa() {{
            const msg = randomMsg(DESPEDIDA);
            respostaDiv.innerHTML = `🧘 ${{msg}}`;
            input.disabled = true;
            button.disabled = true;
            input.value = '';
        }}

        // Função principal para fazer a pergunta
        async function fazerPergunta() {{
            const pergunta = input.value.trim();
            if (!pergunta) return;

            // Verifica se é palavra de saída
            if (PALAVRAS_SAIDA.includes(pergunta.toLowerCase())) {{
                encerrarConversa();
                return;
            }}

            // Feedback visual com mensagem aleatória
            button.classList.add('loading');
            respostaDiv.innerHTML = `<em>${{randomMsg(AGUARDANDO)}}</em>`;

            try {{
                const response = await fetch('/ask', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ pergunta }})
                }});

                const data = await response.json();
                // A resposta já pode conter formatação (quebras de linha)
                respostaDiv.innerHTML = data.resposta.replace(/\\n/g, '<br>');
            }} catch (error) {{
                respostaDiv.innerHTML = '<em>(o vento levou sua pergunta... tente novamente)</em>';
            }} finally {{
                button.classList.remove('loading');
            }}

            input.value = '';  // limpa campo após envio
        }}

        // Event listeners
        button.addEventListener('click', fazerPergunta);
        input.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') fazerPergunta();
        }});
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
    data = await request.json()
    pergunta = data.get("pergunta", "").strip()

    if not pergunta:
        return JSONResponse({"resposta": "(silêncio)"})

    # Tratamento de saída também no backend (fallback)
    if pergunta.lower() in {"sair", "exit", "quit", "gassho", "obrigado"}:
        return JSONResponse({"resposta": random.choice(DESPEDIDA_JS)})

    resposta = responder(pergunta)
    return JSONResponse({"resposta": resposta})

# Para executar diretamente (opcional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)