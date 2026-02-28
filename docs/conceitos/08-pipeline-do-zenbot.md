# Pipeline do ZenBot

Este capítulo descreve **todo o fluxo de funcionamento do ZenBot**, desde a preparação dos textos até a geração da resposta final.

Aqui você verá o ZenBot como um **organismo completo**, e não como partes soltas.

---

## 🧠 O que é um pipeline?

Pipeline é uma **cadeia organizada de etapas**, onde:

> A saída de uma etapa se torna a entrada da próxima.

Em sistemas de IA, o pipeline define:

- Como os dados entram
- Como são processados
- Como viram respostas

---

## 🎯 Objetivo do pipeline do ZenBot

Transformar:

> Livros + textos + perguntas humanas  

em:

> Respostas coerentes, profundas e contextualizadas.

---

## 🧩 Visão geral do pipeline
Textos → Limpeza → Fragmentação → Embeddings → Armazenamento
Pergunta → Embedding → Busca Semântica → Seleção → LLM → Resposta

Ou em forma visual:
Usuário
↓
Pergunta
↓
Embedding
↓
Busca Semântica
↓
Textos Relevantes
↓
LLM (modelo de linguagem)
↓
Resposta Final


---

## 🔹 Etapa 1 — Coleta dos textos

Fontes:

- Livros em PDF
- Textos digitais
- Arquivos Markdown
- Anotações

Objetivo:

> Construir uma base confiável de conhecimento.

---

## 🔹 Etapa 2 — Limpeza dos textos

Scripts utilizados:

- `limpar_texto.py`
- `extrair_pdf.py`

O que acontece:

- Remoção de quebras desnecessárias
- Correção de caracteres estranhos
- Eliminação de ruído visual
- Padronização

Resultado:

> Texto limpo, contínuo e processável.

---

## 🔹 Etapa 3 — Fragmentação (chunking)

Script:

- `fragmentar_texto.py`

O texto é dividido em pequenos blocos chamados **chunks**.

Por quê?

- Modelos trabalham melhor com blocos pequenos
- Permite busca mais precisa
- Evita perda de contexto

Tamanho típico:

- 300 a 800 caracteres

---

## 🔹 Etapa 4 — Geração de embeddings

Script:

- `embeddings.py`

Cada chunk é convertido em um **vetor numérico**.

Resultado:
texto → embedding → vetor

Esses vetores representam o **significado matemático** do conteúdo.

---

## 🔹 Etapa 5 — Armazenamento vetorial

Os embeddings são armazenados em:

- Arquivos `.json`
- Estruturas internas
- Bases vetoriais simples

Arquivo típico:

- `embeddings.json`

Função:

> Permitir busca semântica ultrarrápida.

---

## 🔹 Etapa 6 — Recebimento da pergunta

Via:

- API (interface de comunicação entre sistemas)
- Endpoint `/ask`
- Interface web

Exemplo:

```json
{
  "question": "O que é mente zen?"
}
## 🔹 Etapa 7 — Geração do embedding da pergunta

Quando o usuário envia uma pergunta, o ZenBot **transforma essa pergunta em um vetor numérico**, usando o mesmo modelo de embeddings aplicado aos textos.

Isso garante que:

> Pergunta e textos estejam representados no **mesmo espaço matemático**.

Exemplo conceitual:
"O que é mente zen?" → embedding → vetor numérico

Esse vetor representa o **significado da pergunta**, não apenas suas palavras.

---

## 🔹 Etapa 8 — Busca semântica

Script principal:

- `search.py`

O vetor da pergunta é comparado com **todos os vetores dos textos armazenados**.

O sistema calcula a similaridade entre eles e seleciona:

> Os trechos **mais semanticamente próximos**.

Normalmente são retornados:

- Entre **3 e 8 blocos de texto relevantes**

Isso garante que a resposta seja baseada **em conteúdo real**, e não em improvisação.

---

## 🔹 Etapa 9 — Montagem do contexto

Os trechos encontrados são:

- Organizados
- Concatenados
- Preparados em forma de contexto

Esse contexto é enviado ao modelo de linguagem junto com a pergunta.

Assim, o LLM recebe:

- A pergunta original
- Os textos mais relevantes
- O prompt orientador do ZenBot

Isso cria um **ambiente informacional rico e confiável**.

---

## 🔹 Etapa 10 — Geração da resposta

Script principal:

- `engine.py`

O modelo de linguagem (LLM) recebe:

- Pergunta
- Contexto recuperado
- Prompt do ZenBot

E então:

> Gera uma resposta clara, profunda, didática e coerente com os textos-base.

Essa etapa transforma **informação bruta em linguagem humana compreensível**.

---

## 🔹 Etapa 11 — Retorno da resposta ao usuário

A resposta final é entregue por meio de:

- API (JSON)
- Interface web
- Endpoint `/ask`

Exemplo:

```json
{
  "answer": "A mente zen é o estado de atenção plena..."
}

