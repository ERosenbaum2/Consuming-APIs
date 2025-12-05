# JStory - Story Search System (POC)

A Retrieval-Augmented Generation (RAG) based story search system that helps users find relevant stories from a curated database using semantic search.

## Overview

JStory allows users to search for stories by describing what they're looking for (theme, topic, moral lesson, etc.) rather than using exact keywords. The system uses:

- **Vector Embeddings**: Convert stories into numerical representations that capture semantic meaning
- **ChromaDB**: Vector database for fast similarity search
- **LangChain**: Framework for RAG pipeline implementation
- **OpenAI**: For embeddings and LLM generation
- **Flask**: Web framework for the search interface

## Features

- Semantic story search (find stories by meaning, not just keywords)
- Returns top 3 most relevant stories
- AI-powered analysis explaining why each story matches
- Beautiful, modern web interface
- Local development setup

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection (for initial story download)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Set your OpenAI API key as an environment variable in your terminal session:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

**Alternative:** You can also create a `.env` file in the project root with `OPENAI_API_KEY=your_key_here` if you prefer.

### 3. Download Stories

Run the story collection script to download public domain books:

```bash
python collect_stories.py
```

This will download several story collections from Project Gutenberg:
- Aesop's Fables
- Grimm's Fairy Tales
- Andersen's Fairy Tales
- Arabian Nights
- Just So Stories
- Jataka Tales

The stories will be saved in the `stories/` directory.

### 4. Process Stories and Create Vector Database

Process the downloaded stories, create embeddings, and store them in ChromaDB:

```bash
python process_stories.py
```

This script will:
- Extract individual stories from the downloaded books
- Create embeddings for each story
- Store them in a vector database (`chroma_db/` directory)

**Note**: This step requires your OpenAI API key to be set as an environment variable (or in `.env` file).

### 5. Run the Web Application

Start the Flask server:

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a query describing what kind of story you're looking for
   - Examples:
     - "a story about courage and faith"
     - "a tale with a moral lesson about honesty"
     - "something about friendship and loyalty"
     - "a story where someone overcomes adversity"
3. Click "Search" or press Enter
4. View the top 3 matching stories with AI analysis

## Project Structure

```
.
├── app.py                 # Flask web application
├── collect_stories.py     # Script to download stories
├── process_stories.py     # Script to process stories and create embeddings
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (optional - can use terminal env vars instead)
├── .gitignore           # Git ignore file
├── README.md            # This file
├── stories/             # Downloaded story files (created by collect_stories.py)
├── chroma_db/          # Vector database (created by process_stories.py)
├── templates/          # HTML templates
│   └── index.html      # Main search page
└── static/             # Static files
    └── style.css       # CSS styles
```

## How It Works

### RAG Pipeline

1. **Retrieval**: User query is converted to an embedding and compared with all story embeddings using cosine similarity
2. **Augmentation**: Top 3 matching stories are retrieved and added as context to the prompt
3. **Generation**: An LLM generates a response explaining which stories match and why

### Story Processing

- Stories are extracted from books using pattern matching (chapters, numbered sections, etc.)
- Each story becomes a separate chunk in the vector database
- Very long stories may be split by chapter
- Metadata (source book, story number) is preserved

## Troubleshooting

### "OPENAI_API_KEY not set"
- Make sure you've set `OPENAI_API_KEY` as an environment variable in your terminal session
- Windows PowerShell: `$env:OPENAI_API_KEY="your_key_here"`
- Windows CMD: `set OPENAI_API_KEY=your_key_here`
- Linux/Mac: `export OPENAI_API_KEY='your_key_here'`
- Alternatively, you can create a `.env` file with your API key
- Check that the key is correct and has no extra spaces

### "Vector database not found"
- Run `process_stories.py` first to create the database
- Make sure `chroma_db/` directory exists

### "No story files found"
- Run `collect_stories.py` first to download stories
- Check that `stories/` directory contains `.txt` files

### Stories not extracting properly
- Some books may have different formatting
- You can manually edit the extraction logic in `process_stories.py`
- Or manually split stories and add them to the `stories/` directory

## Future Enhancements

- Add more story collections
- Implement story categorization/tagging
- Add filters (by source, length, theme)
- Support for multiple languages
- User feedback mechanism to improve search quality
- Export stories to PDF/text

## License

This is a proof-of-concept project. Story texts are from public domain sources (Project Gutenberg).

## Credits

Built using:
- [LangChain](https://python.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenAI](https://openai.com/)

