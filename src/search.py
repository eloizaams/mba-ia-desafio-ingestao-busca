import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_store():
      embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))
      store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
      )
      return store

def search_prompt(question=None):
    try:
        store = get_store()
        llm = ChatOpenAI(model="gpt-5-nano", openai_api_key=os.getenv("OPENAI_API_KEY"))
    except Exception as e:
        print(f"Erro ao inicializar LLM ou store: {e}")
        return None

    def ask(query):
        results = store.similarity_search_with_score(query, k=10)
        if not results:
            context = ""
        else:
            context = "\n\n".join([doc.page_content for doc, _ in results])

        prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=query)
        response = llm.invoke(prompt)
        return response.content.strip()

    return ask