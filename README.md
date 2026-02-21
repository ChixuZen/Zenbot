# ZenBot 🧘‍♂️🤖

**ZenBot** é um assistente conversacional baseado em textos clássicos do Zen Budismo, utilizando técnicas modernas de **embeddings, busca semântica e recuperação de contexto (RAG)** para responder perguntas com profundidade, clareza e simplicidade.

O projeto combina filosofia oriental com engenharia de software, criando um chatbot reflexivo, contemplativo e funcional.

---

## 🎯 Objetivo

Criar um chatbot capaz de:

- Consultar textos clássicos do Zen Budismo
- Gerar respostas contextualizadas e semanticamente relevantes
- Oferecer reflexões profundas, coerentes e naturais
- Servir como base para experimentos em **IA, NLP, embeddings e sistemas RAG**

---

## 🧠 Como funciona (Arquitetura)

O ZenBot utiliza um pipeline clássico de **RAG (Retrieval-Augmented Generation)**:


### Fluxo detalhado:

1. **Extração do texto**  
   PDFs são convertidos para texto bruto.

2. **Limpeza**  
   Remoção de ruídos: cabeçalhos, rodapés, símbolos estranhos, duplicações.

3. **Fragmentação (chunking)**  
   O texto é dividido em pequenos trechos semânticos.

4. **Geração de embeddings**  
   Cada fragmento é transformado em vetores numéricos.

5. **Busca semântica**  
   A pergunta do usuário é convertida em embedding e comparada com os fragmentos.

6. **Geração da resposta**  
   Os trechos mais relevantes são usados como contexto para gerar a resposta.

---

## 📂 Estrutura do Projeto
zenbot/
│
├── core/
│ ├── embeddings.py # Geração e carregamento de embeddings
│ ├── search.py # Busca semântica
│ ├── engine.py # Motor principal do chatbot
│ └── init.py
│
├── data/
│ ├── koans.txt
│ └── embeddings.json
│
├── textos/
│ ├── Mente_Zen_Mente_de_Principiante.pdf
│ ├── mente_zen.txt
│ ├── mente_zen_limpo.txt
│ └── chunks.txt
│
├── extrair_pdf.py # Extração de texto do PDF
├── limpar_texto.py # Limpeza do texto
├── fragmentar_texto.py # Geração dos chunks
├── web.py # Interface web (opcional)
├── zen.py # Interface CLI do bot
└── Makefile # Automação do pipeline

## ⚙️ Instalação

### 
1️⃣ Clonar o repositório

```bash
git clone https://github.com/ChixuZen/Zenbot.git
cd zenbot

2️⃣ Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate
3️⃣ Instalar dependências
pip install -r requirements.txt
🚀 Uso
Executar no terminal:
python zen.py
🌐 Interface Web (opcional)
python web.py

Depois acesse:

http://localhost:5000
🧪 Pipeline completo

Você pode rodar todas as etapas automaticamente:

make all

Ou individualmente:

make extrair
make limpar
make fragmentar
make embeddings
📚 Fontes dos Textos

Mente Zen, Mente de Principiante — Shunryu Suzuki

Koans clássicos do Zen Budismo
🛠️ Tecnologias

Python 3.10+

NLP

Embeddings vetoriais

Busca semântica

Arquitetura RAG

🧭 Próximos Passos

Interface gráfica (UI)

Integração com LLMs externos

Persistência vetorial em banco (FAISS, Chroma, etc)

Suporte multi-livros

Ajuste fino de respostas (prompt engineering)

🧘 Filosofia do Projeto

“Na mente do principiante há muitas possibilidades.
Na mente do especialista, poucas.”

Este projeto busca unir tecnologia, contemplação e clareza.

📄 Licença

Este projeto é open-source sob licença MIT.

✨ Autor

Juscelino Lima
Projeto experimental de IA, filosofia e engenharia de software.
