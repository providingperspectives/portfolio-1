import os
from dotenv import load_dotenv

load_dotenv()

from pinecone import Pinecone
from openai import AzureOpenAI
from settings import get_settings

_settings = get_settings()

# Bind directly to your dedicated embedding resource configurations
client = AzureOpenAI(
    api_key=_settings.AZURE_OPENAI_EMBEDDING_KEY,
    api_version=_settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    azure_endpoint=_settings.AZURE_OPENAI_EMBEDDING_ENDPOINT
)

AZURE_DEPLOYMENT = _settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
PINECONE_API_KEY = _settings.PINECONE_API_KEY
PINECONE_INDEX_NAME = _settings.PINECONE_INDEX_NAME

# Keep your identical KNOWLEDGE_BASE array and functions beneath this line.

KNOWLEDGE_BASE = [
    {
        "id": "bio_01",
        "text": "Isiakpona Chuks is an AI Engineer & Systems Architect specializing in autonomous agentic orchestration engines and high-dimensional RAG systems.",
        "category": "biography"
    },
    {
        "id": "proj_mentorqa_01",
        "text": "MentorQA is an automated interaction analysis engine built using FastAPI, Azure OpenAI, and Pinecone. It leverages Hexagonal Architecture to isolate core business scoring criteria from database layers.",
        "category": "projects"
    },
    {
        "id": "proj_ela_01",
        "text": "The English Language Assessment (ELA) Series evolved from ELA-1 to ELA-4, shifting from naive prompts to asynchronous parallel execution pipelines with rigid Pydantic schemas and Pinecone metadata filtering.",
        "category": "projects"
    },
    {
        "id": "stack_01",
        "text": "Chuks' core technical stack includes Python (FastAPI, Flask, Pydantic), JavaScript/TypeScript (React, React Native, Vite), SQL, and Kimball Star Schema data modeling.",
        "category": "skills"
    }
]

def generate_embeddings(text: str) -> list[float]:
    """Generates a dense vector matrix using your deployed Azure OpenAI resource."""
    # Synchronized client instance reference to avoid NameError crashes
    response = client.embeddings.create(
        input=[text],
        model=AZURE_DEPLOYMENT or "text-embedding-3-small"
    )
    return response.data[0].embedding

def seed_vector_store():
    if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
        raise ValueError("Critical System Error: Missing core Pinecone configuration metrics.")
        
    print("Initializing Unified Pinecone client...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    
    vectors_payload = []
    for item in KNOWLEDGE_BASE:
        print(f"Vectorizing payload unit: {item['id']}")
        dense_matrix = generate_embeddings(item['text'])
        
        vectors_payload.append({
            "id": item["id"],
            "values": dense_matrix,
            "metadata": {
                "text": item["text"],
                "category": item["category"]
            }
        })
    
    print(f"Upserting {len(vectors_payload)} items into Pinecone index...")
    index.upsert(vectors=vectors_payload, namespace="portfolio-agent")
    print("Ingestion sequence completed successfully.")

if __name__ == "__main__":
    seed_vector_store()