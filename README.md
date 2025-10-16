# Omni-RAG: Document Question Answering System

A simple yet powerful Retrieval-Augmented Generation (RAG) system that allows you to ask questions about your documents and get AI-powered answers with source citations.

## Overview

This system uses vector embeddings and similarity search to find relevant document chunks, then uses OpenAI's GPT models to generate contextual answers based on the retrieved content.

## Components

### `build_index.py`
Builds a searchable vector index from your documents.

**What it does:**
- Scans the `../data` directory for supported file types (PDF, TXT, MD)
- Extracts text content from documents
- Chunks large documents into manageable pieces (3,500 chars with 400 char overlap)
- Converts text chunks to vector embeddings using sentence-transformers
- Creates a FAISS index for fast similarity search
- Saves the index and metadata for use by `ask.py`

**Output files:**
- `./index/faiss.index` - Vector search index
- `./index/meta.pkl` - Text chunks and metadata

### `ask.py`
Interactive question-answering interface.

**What it does:**
- Loads the pre-built index and metadata
- Takes your question as input
- Finds the most relevant document chunks using vector similarity
- Sends your question + relevant context to OpenAI GPT
- Returns an AI-generated answer with source citations
- Shows similarity scores for transparency

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your documents:**
   - Place PDF, TXT, or MD files in the `rag/data/` directory
   - The system will automatically find and index them

3. **Set up OpenAI API key:**
   - Create a `.env` file in the project root
   - Add: `OPENAI_API_KEY=your_api_key_here`

4. **Build the index:**
   ```bash
   cd rag/index
   python build_index.py
   ```

5. **Ask questions:**
   ```bash
   python ask.py
   ```

## Usage Example

```
Ask: What are the best practices for REST controllers in Java?
```

The system will:
1. Search for relevant chunks in your documents
2. Show similarity scores (0.0-1.0, higher = more relevant)
3. Generate an answer with inline citations like [S1], [S2]
4. List all sources with their similarity scores

## File Structure

```
omni-rag/
├── .env                          # Your OpenAI API key
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── rag/
    ├── data/                     # Put your documents here
    │   └── your-documents.pdf
    └── index/
        ├── build_index.py        # Index builder script
        ├── ask.py               # Question answering script
        └── index/               # Generated index files
            ├── faiss.index      # Vector search index
            └── meta.pkl         # Text chunks and metadata
```

## Dependencies

- **PyPDF2** - PDF text extraction
- **sentence-transformers** - Text to vector embeddings
- **faiss-cpu** - Fast similarity search
- **numpy** - Numerical operations
- **openai** - GPT API access
- **python-dotenv** - Environment variable loading
- **rich** - Beautiful terminal output

## How It Works

1. **Document Processing**: Extracts and chunks text from various file formats
2. **Vectorization**: Converts text chunks to numerical vectors using transformer models
3. **Indexing**: Creates a searchable FAISS index for fast retrieval
4. **Query Processing**: Converts questions to vectors and finds similar chunks
5. **Answer Generation**: Uses GPT to synthesize answers from retrieved context
6. **Citation**: Provides source references and similarity scores

## Tips

- **Better documents = better answers**: Use high-quality, relevant documents
- **Similarity scores**: Scores above 0.7 indicate strong relevance
- **Chunk size**: 3,500 characters with 400-character overlap balances context and precision
- **Model choice**: Uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings and `gpt-4o-mini` for answers

## Troubleshooting

- **"No source files found"**: Check that files are in `rag/data/` with supported extensions
- **"No index found"**: Run `build_index.py` first
- **Low similarity scores**: Your documents might not contain relevant information for the question
- **API errors**: Verify your OpenAI API key in the `.env` file
