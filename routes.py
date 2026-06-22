from flask import Blueprint, request, jsonify
from pinecone import Pinecone
from openai import AzureOpenAI
from settings import get_settings

# Assuming your blueprint is already initialized in your project layout
# main = Blueprint('main', __name__)
from . import main  # Adjust this import to match your project structure

# Initialize your unified configuration object
_settings = get_settings()

# Initialize the Azure OpenAI Client specifically configured for Chat Generation
# This hooks into your main LLM parameters (gpt-4.1-mini)
ai_chat_client = AzureOpenAI(
    api_key=_settings.AZURE_OPENAI_API_KEY,  # Base LLM key
    api_version=_settings.AZURE_OPENAI_API_VERSION,  # 2024-12-01-preview
    azure_endpoint=_settings.AZURE_OPENAI_ENDPOINT
)

# Initialize the Azure OpenAI Client specifically configured for Embedding Retrieval
ai_embed_client = AzureOpenAI(
    api_key=_settings.AZURE_OPENAI_EMBEDDING_KEY,  # Embedding key
    api_version=_settings.AZURE_OPENAI_EMBEDDING_API_VERSION,  # 2024-02-01
    azure_endpoint=_settings.AZURE_OPENAI_EMBEDDING_ENDPOINT
)

@main.route("/api/agent/chat", methods=["POST"])
@limiter.limit("5 per minute")
def agent_chat():
    data = request.get_json() or {}
    user_query = data.get("message", "").strip()
    
    if not user_query:
        return jsonify({"error": "Null payload transmission rejected."}), 400
        
    try:
        # 1. Vectorize the incoming client query using your embedding deployment
        embedding_response = ai_embed_client.embeddings.create(
            input=[user_query],
            model=_settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME  # text-embedding-3-small
        )
        query_vector = embedding_response.data[0].embedding
        
        # 2. Query your live Pinecone index
        pc = Pinecone(api_key=_settings.PINECONE_API_KEY)
        index = pc.Index(_settings.PINECONE_INDEX_NAME)
        
        retrieval_response = index.query(
            namespace="portfolio-agent",
            vector=query_vector,
            top_k=2,              # Pulls the top 2 closest matching professional contexts
            include_metadata=True
        )
        
        # 3. Consolidate retrieved text segments into a single context string
        matches = retrieval_response.get("matches", [])
        context_str = "\n".join([m["metadata"]["text"] for m in matches if "metadata" in m])
        
        # 4. Construct strict, deterministic system instructions guarding against hallucinations
        system_instruction = (
            "You are Chuks' Portfolio AI Assistant, an elite, helpful, and concise AI representative. "
            "You must answer the user's questions using ONLY the verified context provided below. "
            "Do not make up facts, projects, or technical skills outside of this context.\n\n"
            "If the context does not contain enough information to accurately answer the query, "
            "respond exactly with: 'I lack verified systems data to accurately answer this query.'\n\n"
            f"Verified Portfolio Context:\n{context_str}"
        )
        
        # 5. Execute generation via your primary Chat Deployment model
        completion = ai_chat_client.chat.completions.create(
            model=_settings.AZURE_OPENAI_DEPLOYMENT_NAME,  # gpt-4.1-mini
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.2  # Low temperature ensures high determinism and adherence to context
        )
        
        agent_response = completion.choices[0].message.content
        
        # Return a clean JSON response back to the client interface
        return jsonify({
            "response": agent_response,
            "sources_consulted": len(matches)
        }), 200
        
    except Exception as e:
        # Log the full traceback internally for architectural debugging
        print(f"RAG Inference Pipeline Failure: {str(e)}")
        return jsonify({"error": "Internal execution pipeline failure."}), 500