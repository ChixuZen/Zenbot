# 08 – Organização dos Textos no Projeto ZenBot

Este documento descreve como os textos são organizados, tratados e preparados para se tornarem a **base de conhecimento do ZenBot**.

O objetivo é transformar conteúdos brutos em **informação estruturada, pesquisável e semanticamente significativa**.

---

## 1. Visão Geral

O ZenBot utiliza textos como fonte principal de conhecimento. Esses textos passam por um **processo de transformação**, que inclui:

Texto bruto → Limpeza → Fragmentação → Embeddings → Busca Semântica

Esse fluxo garante que o sistema consiga **entender o significado dos conteúdos**, e não apenas localizar palavras.

---

## 2. Tipos de Textos Utilizados

Os principais formatos são:

- PDFs
- Arquivos de texto (.txt)
- Textos extraídos da web
- Conteúdos preparados manualmente

Esses materiais ficam organizados principalmente na pasta:
textos/

---

## 3. Limpeza dos Textos

Após a extração, os textos passam por um processo de **limpeza**, que inclui:

- Remoção de caracteres estranhos.
- Correção de espaçamentos.
- Padronização de parágrafos.
- Eliminação de ruídos visuais.

Objetivo: deixar o texto **mais claro, contínuo e semanticamente consistente**.

---

## 4. Fragmentação (Chunks)

Textos longos são divididos em **pequenos blocos**, chamados de *chunks*.

### Por que fragmentar?

- Facilita a indexação.
- Melhora a busca semântica.
- Permite respostas mais precisas.

Cada chunk representa uma **ideia completa ou um pequeno trecho coerente**.

---

## 5. Geração de Embeddings

Cada fragmento é convertido em um **vetor semântico (embedding)**.

Embeddings são **representações matemáticas do significado dos textos**, permitindo que o sistema:

- Compare ideias.
- Meça similaridade.
- Realize busca por sentido, e não apenas por palavras.

---

## 6. Armazenamento dos Dados

Os dados gerados são organizados principalmente em:
data/

Contendo:

- Vetores de embeddings.
- Índices de busca.
- Arquivos auxiliares para desempenho.

---

## 7. Pipeline de Preparação dos Textos

O processo completo segue a sequência:

1. Extração do texto.
2. Limpeza.
3. Fragmentação.
4. Geração dos embeddings.
5. Armazenamento.
6. Indexação para busca.

Este conjunto de etapas forma o **pipeline de preparação do conhecimento**.

---

## 8. Organização dos Arquivos

A separação clara entre:

- Textos brutos
- Textos limpos
- Fragmentos
- Dados vetoriais

permite:

- Facilidade de manutenção.
- Reprocessamento simples.
- Evolução contínua da base de conhecimento.

---

## 9. Princípios da Organização

- Clareza  
- Simplicidade  
- Modularidade  
- Reprodutibilidade  
- Qualidade semântica  

---

## 10. Conclusão

A organização dos textos é o **coração do ZenBot**. Um bom preparo dos dados garante:

- Respostas melhores.
- Maior coerência.
- Melhor experiência para o usuário.
- Base sólida para evolução futura.