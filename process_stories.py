"""
Script to process story files, split them into chunks (one story per chunk),
create embeddings, and store them in ChromaDB.
"""

import os
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
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

def extract_stories_from_file(filepath):
    """
    Extract individual stories from a text file.
    Each story is identified by patterns like:
    - Chapter headings
    - Story titles (numbered or titled)
    - Section breaks
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Project Gutenberg header/footer
    content = re.sub(r'\*\*\*.*?END.*?\*\*\*', '', content, flags=re.DOTALL)
    content = re.sub(r'Project Gutenberg.*?www\.gutenberg\.org.*?\n', '', content, flags=re.DOTALL)
    
    stories = []
    filename = Path(filepath).stem
    
    # Try different patterns to split stories
    # Pattern 1: Chapter headings (CHAPTER I, Chapter 1, etc.)
    chapter_pattern = r'(?i)(?:^|\n)(?:CHAPTER|Chapter)\s+[IVXLCDM0-9]+[\.:]?\s*\n'
    # Pattern 2: Numbered stories (1., 2., etc.)
    numbered_pattern = r'(?i)(?:^|\n)\d+[\.\)]\s+[A-Z]'
    # Pattern 3: Story titles in all caps or with specific formatting
    title_pattern = r'(?i)(?:^|\n)(?:THE\s+)?[A-Z][A-Z\s]{10,}\n'
    
    # Try chapter pattern first
    chapters = re.split(chapter_pattern, content)
    if len(chapters) > 2:  # If we found chapters
        for i, chapter in enumerate(chapters[1:], 1):
            chapter = chapter.strip()
            if len(chapter) > 100:  # Minimum story length
                stories.append({
                    'text': chapter,
                    'source': filename,
                    'story_id': f"{filename}_chapter_{i}",
                    'metadata': {'source': filename, 'type': 'chapter', 'number': i}
                })
    
    # If no chapters found, try numbered stories
    if len(stories) < 3:
        numbered = re.split(numbered_pattern, content)
        if len(numbered) > 2:
            stories = []
            for i, story in enumerate(numbered[1:], 1):
                story = story.strip()
                if len(story) > 100:
                    stories.append({
                        'text': story,
                        'source': filename,
                        'story_id': f"{filename}_story_{i}",
                        'metadata': {'source': filename, 'type': 'story', 'number': i}
                    })
    
    # If still no stories, split by large paragraph breaks
    if len(stories) < 3:
        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r'\n\n+', content)
        # Group paragraphs into stories (stories are typically 3+ paragraphs)
        current_story = []
        story_num = 1
        
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50:
                current_story.append(para)
                # If we have enough paragraphs, make it a story
                if len(current_story) >= 3 and len('\n\n'.join(current_story)) > 500:
                    story_text = '\n\n'.join(current_story)
                    stories.append({
                        'text': story_text,
                        'source': filename,
                        'story_id': f"{filename}_story_{story_num}",
                        'metadata': {'source': filename, 'type': 'story', 'number': story_num}
                    })
                    current_story = []
                    story_num += 1
        
        # Add remaining paragraphs as last story
        if current_story and len('\n\n'.join(current_story)) > 500:
            story_text = '\n\n'.join(current_story)
            stories.append({
                'text': story_text,
                'source': filename,
                'story_id': f"{filename}_story_{story_num}",
                'metadata': {'source': filename, 'type': 'story', 'number': story_num}
            })
    
    # If still no good splits, treat entire file as one story (split by chapters if too long)
    if len(stories) < 3:
        if len(content) > 10000:
            # Split very long content into chapters
            chunk_size = 5000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            stories = []
            for i, chunk in enumerate(chunks, 1):
                if len(chunk.strip()) > 500:
                    stories.append({
                        'text': chunk.strip(),
                        'source': filename,
                        'story_id': f"{filename}_chunk_{i}",
                        'metadata': {'source': filename, 'type': 'chunk', 'number': i}
                    })
        else:
            # Single story
            stories = [{
                'text': content.strip(),
                'source': filename,
                'story_id': f"{filename}_complete",
                'metadata': {'source': filename, 'type': 'complete'}
            }]
    
    return stories

def process_all_stories():
    """Process all story files and create vector database."""
    print("=" * 60)
    print("JStory - Story Processing Script")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("\n⚠️  ERROR: OPENAI_API_KEY not set as environment variable")
        print("Please set OPENAI_API_KEY in your terminal session.")
        print("Windows PowerShell: $env:OPENAI_API_KEY='your_key_here'")
        print("Windows CMD: set OPENAI_API_KEY=your_key_here")
        return
    
    # Get all story files
    story_dir = Path("stories")
    if not story_dir.exists():
        print(f"\n⚠️  ERROR: Stories directory not found!")
        print("Please run collect_stories.py first to download stories.")
        return
    
    story_files = list(story_dir.glob("*.txt"))
    if not story_files:
        print(f"\n⚠️  ERROR: No story files found in {story_dir}")
        print("Please run collect_stories.py first to download stories.")
        return
    
    print(f"\nFound {len(story_files)} story files")
    print("Extracting stories from files...\n")
    
    # Extract all stories
    all_stories = []
    for filepath in story_files:
        print(f"Processing {filepath.name}...")
        stories = extract_stories_from_file(filepath)
        print(f"  ✓ Extracted {len(stories)} stories/chapters")
        all_stories.extend(stories)
    
    print(f"\nTotal stories extracted: {len(all_stories)}")
    
    if len(all_stories) < 200:
        print(f"\n⚠️  WARNING: Only {len(all_stories)} stories found. Target is 200+.")
        print("You may want to download more books or adjust extraction logic.")
    
    # Create LangChain Documents
    documents = []
    for story in all_stories:
        doc = Document(
            page_content=story['text'],
            metadata=story['metadata']
        )
        documents.append(doc)
    
    # Initialize embeddings
    print("\nInitializing OpenAI embeddings...")
    # SSL verification is disabled globally via httpx patch above
    # This allows OpenAIEmbeddings to create its own client internally
    embeddings = OpenAIEmbeddings()
    
    # Create vector store
    print("Creating vector database...")
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print(f"\n✓ Successfully created vector database with {len(documents)} stories!")
    print("✓ Database saved to ./chroma_db")
    print("\n" + "=" * 60)
    print("Ready to use! You can now run the Flask app with: python app.py")
    print("=" * 60)

if __name__ == "__main__":
    process_all_stories()

