# Desafio MBA Engenharia de Software com IA - Full Cycle  
## Ingestão e Busca Semântica com LangChain e Postgres

Este projeto realiza a ingestão de um arquivo PDF em um banco PostgreSQL com extensão pgVector e permite buscas semânticas via linha de comando, utilizando LangChain e modelos de embeddings/LLM da OpenAI.

---

## Objetivo

- Ler um PDF, dividir em chunks, gerar embeddings e armazenar no Postgres/pgVector.
- Permitir buscas semânticas via CLI, respondendo apenas com base no conteúdo do PDF.

---

## Requisitos

- Python 3.12.3 (recomendado uso de virtualenv)
- Docker e Docker Compose
- Conta e API Key da OpenAI

---

## Instalação

1. **Clone o repositório e acesse a pasta do projeto:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <PASTA_DO_PROJETO>
    ```

2. **Crie e ative o ambiente virtual:**

    ```bash
    python3 -m venv venv312
    source venv312/bin/activate  # Linux/Mac
    # venv312\Scripts\activate   # Windows
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis de ambiente:**

    - Copie o arquivo `.env.example` para `.env`:

        ```bash
        cp .env.example .env
        ```

    - Edite o arquivo `.env` com seus dados:

        ```env
        OPENAI_API_KEY="sua api key"
        OPENAI_EMBEDDING_MODEL=text-embedding-3-small
        DATABASE_URL=postgresql+psycopg://postgres:postgres@host.docker.internal:5432/rag
        PG_VECTOR_COLLECTION_NAME=gpt5_collection
        PDF_PATH=document.pdf
        ```

---

## Execução

1. **Suba o banco de dados com Docker Compose:**

    ```bash
    docker compose up -d
    ```

2. **Ingestão do PDF (gera embeddings e armazena no banco):**

    ```bash
    python src/ingest.py
    ```

3. **Inicie o chat para perguntas e respostas:**

    ```bash
    python src/chat.py
    ```

---

## Exemplo de uso

Faça sua pergunta:

**PERGUNTA:** Qual o faturamento da Empresa SuperTechIABrazil?  
**RESPOSTA:** O faturamento foi de 10 milhões de reais.

---

### Perguntas fora do contexto

**PERGUNTA:** Quantos clientes temos em 2024?  
**RESPOSTA:** Não tenho informações necessárias para responder sua pergunta.

---

## Observações

- O sistema responde apenas com base no conteúdo do PDF ingerido.
- Perguntas fora do contexto retornam:  
  `Não tenho informações necessárias para responder sua pergunta.`

---

