# Evolução do Projeto ZenBot

Este documento descreve a evolução do projeto **ZenBot**, desde sua concepção inicial até os estágios atuais de desenvolvimento.

O objetivo é registrar:
- O raciocínio por trás das decisões técnicas.
- Os problemas enfrentados.
- As soluções adotadas.
- As mudanças de direção ao longo do tempo.
- Os aprendizados adquiridos.

Esse histórico serve tanto para **documentação técnica**, quanto para **onboarding de novos colaboradores**, além de permitir revisitar decisões passadas e entender melhor o caminho seguido.

---

## 1. Motivação Inicial

O ZenBot nasceu da necessidade de criar um **assistente inteligente, modular e evolutivo**, capaz de:

- Integrar múltiplas ferramentas.
- Consultar bases de conhecimento próprias.
- Evoluir com o tempo.
- Facilitar automações e organização de informações.
- Servir como laboratório prático para aprendizado em:
  - Inteligência Artificial
  - Arquitetura de software
  - Sistemas distribuídos
  - DevOps
  - Processamento de linguagem natural (PLN)

A ideia central sempre foi **aprender construindo**, documentando cada passo.

---

## 2. Primeiras Ideias e Explorações

Nos estágios iniciais, o projeto focou em:

- Entender como funcionam modelos de linguagem (LLMs).
- Explorar APIs de IA.
- Criar pequenos protótipos de chatbots.
- Testar diferentes arquiteturas.

Essa fase foi marcada por:
- Muitos testes.
- Código experimental.
- Mudanças frequentes.
- Aprendizado acelerado.

---

## 3. Definição da Arquitetura Base

Com a maturação das ideias, surgiu a necessidade de:

- Organizar melhor o projeto.
- Separar responsabilidades.
- Definir padrões claros.

Principais decisões:

- Separação entre:
  - Backend (lógica do bot)
  - Camada de IA
  - Armazenamento
  - Interface
- Uso de APIs externas (ex: APIs, *interfaces de programação de aplicações*, de modelos de IA).
- Estrutura modular para facilitar evolução e manutenção.

---

## 4. Organização do Repositório

Foi criada uma estrutura de pastas clara, visando:

- Facilidade de navegação.
- Separação lógica entre documentação, código e dados.
- Facilidade de publicação.

Principais diretórios:

- `/docs` → documentação geral do projeto
- `/docs/conceitos` → explicação de conceitos técnicos
- `/docs/registros` → registros históricos e templates
- Outras pastas voltadas ao código-fonte e serviços

---

## 5. Introdução da Documentação em Markdown

A documentação passou a ser escrita em **Markdown**, pois:

- É simples.
- É legível em texto puro.
- Funciona bem com GitHub.
- Permite fácil publicação como site estático.

Com isso, adotou-se o padrão:

- Um arquivo por tema.
- Índices claros.
- Numeração lógica.
- Organização progressiva.

---

## 6. Evolução da Ideia de Base de Conhecimento

Surgiu então a necessidade de:

- Armazenar conhecimento do próprio projeto.
- Criar documentação acessível tanto para humanos quanto para IAs.
- Permitir futuras integrações com:
  - Busca semântica
  - Embeddings (representações vetoriais de textos)
  - Bancos vetoriais

Esse movimento marcou a transição de um simples chatbot para um **sistema inteligente orientado a conhecimento**.

---

## 7. Introdução de Conceitos Avançados

Ao longo da evolução, passaram a ser estudados e integrados conceitos como:

- Modelos de linguagem (LLMs, *Large Language Models*).
- Embeddings (vetorização semântica de textos).
- Busca semântica.
- Pipelines de processamento.
- Arquiteturas de agentes.
- Orquestração de fluxos de IA.

Esses conceitos estão documentados detalhadamente na pasta:

```text
docs/conceitos