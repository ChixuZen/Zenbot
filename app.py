from fastapi import FastAPI
from pydantic import BaseModel
from core.engine import buscar_blocos  # função que responde às perguntas

app = FastAPI(title="ZenBot API")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "ZenBot online"}

@app.post("/ask")
def ask(q: Query):
    # buscar_blocos retorna uma lista de respostas, pegamos a primeira
    respostas = buscar_blocos(q.question)
    resposta = respostas[0] if respostas else "Nada a responder."
    return {"question": q.question, "answer": resposta}
