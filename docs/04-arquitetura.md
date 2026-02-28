# 04 – Arquitetura do Projeto ZenBot

Este documento descreve, de forma simples e didática, como o ZenBot está organizado internamente e como seus componentes se conectam.

---

## 1. Visão Geral da Arquitetura

O ZenBot segue uma arquitetura modular, organizada em camadas, com o objetivo de:

- Facilitar o entendimento do sistema.
- Tornar o código mais limpo.
- Permitir evolução e manutenção contínua.

De forma resumida, o fluxo principal é:

Usuário → API Web → Busca Semântica → Geração de Resposta → Usuário

---

## 2. Estrutura Geral de Pastas

A estrutura principal do projeto é:
```text
zenbot/
├── core/
├── data/
├── textos/
├── scripts/
├── docs/
├── web.py
├── zen.py
└── Makefile
```

Cada pasta possui uma função específica dentro do sistema.

---

## 3. Camada de Interface (API Web)

A interface com o usuário ocorre por meio de uma **API Web**, construída com FastAPI (framework web em Python).

Funções principais:

- Receber perguntas via HTTP (protocolo de comunicação web).
- Enviar a pergunta para o motor interno.
- Retornar a resposta ao usuário.

Arquivos principais:
- `web.py`
- `zen.py`

---

## 4. Camada de Processamento Central (core)

A pasta `core/` contém o núcleo lógico do ZenBot.
```text
core/
├── embeddings.py
├── search.py
└── engine.py
```

### Função de cada módulo:

- **embeddings.py**  
  Responsável por gerar vetores semânticos (embeddings, ou representações matemáticas do significado dos textos).

- **search.py**  
  Realiza a busca semântica (busca por significado, e não apenas por palavras-chave), encontrando os trechos mais relevantes.

- **engine.py**  
  Coordena todo o processo:  
  pergunta → busca → montagem do contexto → resposta final.

---

## 5. Camada de Dados e Textos

### Pasta `textos/`

Contém os textos-base usados como fonte de conhecimento, tais como:

- PDFs
- Textos limpos
- Fragmentos (chunks, ou pedaços menores de texto)

### Pasta `data/`

Armazena:

- Arquivos de embeddings.
- Índices vetoriais.
- Dados intermediários usados para acelerar as buscas.

---

## 6. Camada de Scripts Auxiliares

A pasta `scripts/` contém ferramentas para:

- Extração de texto de PDF.
- Limpeza textual.
- Fragmentação em blocos menores.
- Preparação dos dados para geração de embeddings.

Esses scripts formam o **pipeline de preparação do conhecimento**.

---

## 7. Fluxo Simplificado de Funcionamento

1. O usuário faz uma pergunta.
2. A API recebe a requisição.
3. O motor central (`engine`) processa a pergunta.
4. O sistema de busca localiza os trechos mais relevantes.
5. O contexto é montado.
6. A IA gera a resposta.
7. A resposta retorna ao usuário.

---

## 8. Princípios de Arquitetura

- Simplicidade  
- Modularidade  
- Clareza  
- Facilidade de evolução  
- Foco educacional  

---

## 9. Conclusão

A arquitetura do ZenBot foi pensada não apenas para funcionar, mas também para **ensinar**, permitindo que qualquer pessoa possa compreender seu funcionamento interno e contribuir com melhorias.
Quando quiser, seguimos no mesmo ritmo calmo com:
