from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from pinecone import Pinecone
from openai import AzureOpenAI
from settings import get_settings

main = Blueprint("main", __name__)

# Initialize your unified configuration object
# Initialize your unified configuration object
_settings = get_settings()

# Initialize the Azure OpenAI Client specifically configured for Chat Generation
ai_chat_client = AzureOpenAI(
    api_key=_settings.AZURE_OPENAI_KEY,  # <-- MATCHES YOUR .env KEY FOR CHAT
    api_version=_settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=_settings.AZURE_OPENAI_ENDPOINT
)

# Initialize the Azure OpenAI Client specifically configured for Embedding Retrieval
ai_embed_client = AzureOpenAI(
    api_key=_settings.AZURE_OPENAI_EMBEDDING_KEY, # <-- MATCHES YOUR .env KEY FOR EMBEDDINGS
    api_version=_settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    azure_endpoint=_settings.AZURE_OPENAI_EMBEDDING_ENDPOINT
)

@main.route("/")
def home():
    country = request.args.get("country")
    source = request.args.get("source")  
    return render_template("index.html", country=country, source=source)

@main.route("/about")
def about():
    context = {
        "biography": (
            "I am an AI Engineer and Full-Stack Developer focused on building robust autonomous execution layers "
            "and complex data retrieval environments. My engineering philosophy centers around clean software "
            "abstractions—using Domain-Driven Design (DDD) and Hexagonal Architecture to isolate core business rules "
            "from infrastructure layers. Moving from raw full-stack development into specialized intelligent automation, "
            "I build resilient software designed for high-throughput predictability."
        )
    }
    return render_template("about.html", context=context)

@main.route('/about-us')
def about_us():
    return redirect(url_for("main.about"))

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # Server-side logging placeholder
        print(f"Contact form submitted: {name} <{email}>: {message}")
        return redirect(url_for('main.contact', sent=1))
    return render_template("contact.html")

@main.route("/portfolio")
def portfolio():
    # Production implementations mapping arrays for template cards
    projects_list = [
        {
            'name': 'MentorQA Evaluation Engine', 
            'description': 'An automated interaction analysis pipeline leveraging Retrieval-Augmented Generation (RAG) models to evaluate transcripts against strict professional quality matrices.', 
            'endpoint': 'mentor-qa', 
            'image': 'mentor-qa.svg',
            'stack': ['FastAPI', 'Azure OpenAI', 'Pinecone', 'React TSX'],
            'architecture': 'Hexagonal Pattern'
        },
        {
            'name': 'English Language Assessment Series', 
            'description': 'Iterative NLP grading architectures (ELA-1 through ELA-4) utilizing dense semantic embedding matching and vector storage pipelines for automated contextual rubric execution.', 
            'endpoint': 'grader-function', 
            'image': 'grader_system.svg',
            'stack': ['Python Async', 'Pinecone DB', 'Pydantic', 'Flask'],
            'architecture': 'Domain-Driven Design'
        },
        {
            'name': 'Multiplan Agribusiness Hub', 
            'description': 'Full-stack operational infrastructure designed for Multiplan Agro-Culture Farms, combining automated client workflows with rigorous data validation rules.', 
            'endpoint': 'multiplan-agro', 
            'image': 'multiplan.svg',
            'stack': ['React', 'Python', 'DNS SEC', 'SQL'],
            'architecture': 'Clean Monolith'
        }
    ]
    return render_template("portfolio.html", projects=projects_list)

@main.route("/portfolio/<project>")
def project(project):
    # Route mappings matching your elite architectural endpoints
    valid_projects = ["mentor-qa", "grader-function", "multiplan-agro"]
    if project in valid_projects:
        return render_template(f"portfolio/{project}.html")
    return redirect(url_for("main.not_found_404"))
    
@main.route('/portfolio/json')
def portfolio_json():
    # Replaces placeholders with production system descriptors
    projects = {
        "mentor-qa": {
            "language": "python",
            "orchestration": "fastapi",
            "embeddings": "azure-openai",
            "vector_store": "pinecone",
            "status": "active"
        },
        "grader-function": {
            "language": "python",
            "validation": "pydantic",
            "vector_store": "pinecone",
            "status": "iterating"
        }
    }
    return jsonify(projects)

# ─── AGENTIC INFERENCE PIPELINE ENDPOINT ─────────────────────────────────────
@main.route("/api/agent/chat", methods=["POST"])
def agent_chat():
    data = request.get_json() or {}
    user_query = data.get("message", "").strip()
    
    if not user_query:
        return jsonify({"error": "Null payload transmission rejected."}), 400
        
    try:
        # 1. Vectorize the incoming client query using your embedding deployment
        embedding_response = ai_embed_client.embeddings.create(
            input=[user_query],
            model=_settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
        )
        query_vector = embedding_response.data[0].embedding
        
        # 2. Query your live Pinecone index
        pc = Pinecone(api_key=_settings.PINECONE_API_KEY)
        index = pc.Index(_settings.PINECONE_INDEX_NAME)
        
        retrieval_response = index.query(
            namespace="portfolio-agent",
            vector=query_vector,
            top_k=2,
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
            model=_settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ],
            temperature=0.2
        )
        
        agent_response = completion.choices[0].message.content
        
        return jsonify({
            "response": agent_response,
            "sources_consulted": len(matches)
        }), 200
        
    except Exception as e:
        print(f"RAG Inference Pipeline Failure: {str(e)}")
        return jsonify({"error": "Internal execution pipeline failure."}), 500

@main.route("/s")
def search():
    keyword = request.args.get("k")
    return f"{keyword}" if keyword else "No query specified."

@main.route('/404')
def not_found_404():
    return render_template("404.html"), 404

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404