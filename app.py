"""
Flask web application for JStory - Story Search System using RAG.
"""

import os
from flask import Flask, render_template, request, jsonify
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Load environment variables (optional - will work with terminal env vars too)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not needed if using terminal environment variables

# Configure SSL certificates for Windows
# This must be done BEFORE importing httpx or OpenAI clients
try:
    import certifi
    import ssl
    # Set SSL certificate path for httpx/requests
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['HTTPX_CA_BUNDLE'] = certifi.where()
except ImportError:
    pass  # certifi not available, will use default

# For Windows SSL certificate issues, patch httpx to disable verification globally
# WARNING: This is NOT secure and should only be used for local POC development
# In production, you should properly configure SSL certificates
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Patch httpx to use verify=False by default (POC workaround)
try:
    import httpx
    _original_client_init = httpx.Client.__init__
    def _patched_client_init(self, *args, verify=None, **kwargs):
        if verify is None:
            verify = False  # Disable SSL verification for POC
        return _original_client_init(self, *args, verify=verify, **kwargs)
    httpx.Client.__init__ = _patched_client_init
    
    # Also patch AsyncClient
    _original_async_client_init = httpx.AsyncClient.__init__
    def _patched_async_client_init(self, *args, verify=None, **kwargs):
        if verify is None:
            verify = False  # Disable SSL verification for POC
        return _original_async_client_init(self, *args, verify=verify, **kwargs)
    httpx.AsyncClient.__init__ = _patched_async_client_init
except Exception:
    pass  # If patching fails, continue anyway

app = Flask(__name__)

# Initialize components
embeddings = None
vector_store = None
llm = None
initialization_error = None

def initialize_components():
    """Initialize embeddings, vector store, and LLM."""
    global embeddings, vector_store, llm, initialization_error
    
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY not set as environment variable")
        
        # Initialize embeddings and LLM
        # SSL verification is disabled globally via httpx patch above
        # This allows OpenAIEmbeddings and ChatOpenAI to create their own clients internally
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        # Load vector store
        chroma_path = "./chroma_db"
        if not os.path.exists(chroma_path):
            raise ValueError(f"Vector database not found at {chroma_path}! The chroma_db directory must be included in your deployment. Check that it's not in .gitignore and is committed to your repository.")
        
        vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )
        
        initialization_error = None
        print("✓ Components initialized successfully")
    except Exception as e:
        initialization_error = str(e)
        print(f"✗ Error initializing application: {e}")
        raise

def search_stories(query, k=3):
    """
    Search for stories using RAG.
    Returns top k matching stories.
    """
    if not vector_store:
        raise ValueError("Vector store not initialized")
    
    # Step 1: RETRIEVE - Find similar stories
    results = vector_store.similarity_search_with_score(query, k=k)
    
    # Format results
    stories = []
    for doc, score in results:
        stories.append({
            'text': doc.page_content,
            'source': doc.metadata.get('source', 'Unknown'),
            'type': doc.metadata.get('type', 'story'),
            'number': doc.metadata.get('number', 'N/A'),
            'similarity_score': float(score)
        })
    
    return stories

def generate_response(query, stories):
    """
    Generate a response using RAG (Retrieval-Augmented Generation).
    """
    if not llm:
        raise ValueError("LLM not initialized")
    
    # Step 2: AUGMENT - Build context from retrieved stories
    context = ""
    for i, story in enumerate(stories, 1):
        context += f"\n\n--- Story {i} (from {story['source']}) ---\n"
        # Truncate very long stories for context
        story_text = story['text']
        if len(story_text) > 2000:
            story_text = story_text[:2000] + "..."
        context += story_text
    
    # Step 3: GENERATE - Create prompt and call LLM
    prompt = f"""Based on the following stories retrieved from a database, please provide a helpful response to the user's query.

User Query: {query}

Retrieved Stories:
{context}

Please:
1. Identify which story (or stories) best match the user's query
2. Provide a brief summary of why each story is relevant
3. If multiple stories match, explain how they relate to the query

Keep your response concise and focused on helping the user find the right story."""
    
    response = llm.invoke(prompt)
    return response.content

@app.route('/')
def index():
    """Render the main search page."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle story search requests."""
    global initialization_error
    
    # Check if initialization failed
    if initialization_error:
        return jsonify({
            'error': f'Application not initialized: {initialization_error}'
        }), 503
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Ensure components are initialized
        if not vector_store:
            return jsonify({
                'error': 'Vector store not initialized. Please check server logs for initialization errors.'
            }), 503
        
        # Search for top 3 matching stories
        stories = search_stories(query, k=3)
        
        # Generate RAG response
        rag_response = generate_response(query, stories)
        
        return jsonify({
            'success': True,
            'query': query,
            'stories': stories,
            'rag_response': rag_response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        if vector_store is None:
            return jsonify({'status': 'not_ready', 'message': 'Vector store not initialized'}), 503
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Initialize components when the app starts (works with both Flask dev server and gunicorn)
print("Initializing JStory application...")
try:
    initialize_components()
except Exception as e:
    print(f"\n✗ Error initializing application: {e}")
    print("\nPlease ensure:")
    print("  1. You have set OPENAI_API_KEY as an environment variable")
    print("  2. The chroma_db directory exists and is included in your deployment")
    print("  3. If chroma_db is in .gitignore, remove it and commit the directory to your repository")

if __name__ == '__main__':
    # Development server only
    port = int(os.getenv('PORT', 5000))
    print("\n" + "=" * 60)
    print("JStory is ready!")
    print("=" * 60)
    print(f"\nStarting Flask server on port {port}...")
    print("Open your browser to: http://localhost:" + str(port))
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=False, host='0.0.0.0', port=port)

