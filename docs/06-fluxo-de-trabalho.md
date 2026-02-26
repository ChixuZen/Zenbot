# 06 – Fluxo de Trabalho do Projeto ZenBot

Este documento descreve o **passo a passo básico do trabalho diário no projeto ZenBot**, desde o desenvolvimento local até o deploy em produção.

O objetivo é manter um fluxo simples, previsível e organizado.

---

## 1. Visão Geral do Fluxo

O ciclo básico de trabalho segue esta sequência:
Planejar → Codar → Testar Local → Versionar → Publicar → Testar Produção

---

## 2. Desenvolvimento Local

Nesta etapa, todo o trabalho acontece na máquina local.

Principais atividades:

- Criar ou modificar código.
- Ajustar scripts.
- Atualizar textos e dados.
- Organizar a documentação.

Ferramentas principais:

- Editor de código
- Terminal
- Python
- Ambiente virtual (venv)

---

## 3. Testes Locais

Antes de publicar qualquer alteração, o sistema é testado localmente.

Principais formas de teste:

- Execução direta via terminal.
- Uso de `curl` para simular requisições HTTP.
- Testes via navegador.
- Exposição temporária com ngrok.

Objetivo:

- Garantir que tudo funciona antes de publicar.

---

## 4. Versionamento com Git

Após os testes locais:

1. Os arquivos são adicionados ao Git.
2. Um commit é criado com uma mensagem clara.
3. As alterações são enviadas ao GitHub.

Objetivo:

- Manter histórico.
- Garantir backup.
- Organizar evolução do projeto.

---

## 5. Deploy no Render

Com o código atualizado no GitHub, o Render:

- Detecta automaticamente mudanças.
- Executa o processo de build.
- Publica a nova versão.

Objetivo:

- Tornar as alterações acessíveis publicamente.

---

## 6. Testes em Produção

Após o deploy:

- Testes são feitos diretamente no endereço público.
- Logs são monitorados.
- Possíveis erros são corrigidos.

---

## 7. Registro das Evoluções

Sempre que possível, as mudanças importantes são:

- Documentadas em Markdown.
- Registradas na pasta `docs/`.
- Incluídas no histórico do projeto.

---

## 8. Princípios do Fluxo de Trabalho

- Simplicidade  
- Clareza  
- Organização  
- Aprendizado contínuo  
- Evolução gradual  

---

## 9. Conclusão

Este fluxo de trabalho permite que o ZenBot evolua de forma **organizada, segura e didática**, favorecendo tanto o aprendizado quanto a estabilidade do sistema.