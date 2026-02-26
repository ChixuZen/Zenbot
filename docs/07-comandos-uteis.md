# 07 – Comandos Úteis do Projeto ZenBot

Este documento reúne os **principais comandos utilizados no dia a dia do desenvolvimento do ZenBot**, servindo como uma "cola rápida" para consulta.

---

## 1. Navegação no Terminal

```bash
pwd            # Mostra o diretório atual
ls             # Lista arquivos e pastas
cd pasta       # Entra em uma pasta
cd ..          # Volta um nível
mkdir nome     # Cria uma nova pasta

2. Ambiente Virtual Python (venv)
python3 -m venv venv     # Cria ambiente virtual
source venv/bin/activate # Ativa o ambiente virtual
deactivate               # Desativa o ambiente virtual

3. Instalação de Dependências
pip install pacote       # Instala um pacote
pip install -r requirements.txt  # Instala dependências do projeto
pip freeze > requirements.txt    # Salva lista de dependências

4. Execução do Servidor Local
uvicorn web:app --reload
Cria uma URL pública temporária para testes externos.

5. Testes via Curl
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"O que é a mente zen?"}'

  7. ngrok — Exposição Temporária
  ngrok http 8000

  8. Render — Deploy
  O deploy ocorre automaticamente após o git push.

  9. Organização dos Arquivos

  tree docs            # Mostra árvore de arquivos (se instalado)
find . -type f       # Lista todos os arquivos

10. Dicas Gerais

Sempre ativar o venv antes de rodar o projeto.

Testar localmente antes do deploy.

Fazer commits pequenos e frequentes.

Manter a documentação atualizada.