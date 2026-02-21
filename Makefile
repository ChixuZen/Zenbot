.PHONY: run web ollama chat pull

run:
	python zen.py

web:
	uvicorn web:app --reload

pull:
	ollama pull llama3.1:8b
	ollama pull nomic-embed-text

ollama:
	ollama run llama3.1:8b

chat:
	python chat.py
