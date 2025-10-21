# Docker Setup for Omni-RAG System

This guide will help you run the RAG system in a Docker container, which solves dependency and proxy issues.

## Prerequisites

1. **Docker Desktop** installed on your Windows machine
2. **Docker Compose** (usually comes with Docker Desktop)

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the project root with your settings:

```bash
# Proxy settings (replace with your actual proxy URLs)
HTTP_PROXY=http://your-proxy-server:port
HTTPS_PROXY=http://your-proxy-server:port
NO_PROXY=localhost,127.0.0.1

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Build and Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Start the container
docker-compose up -d

# Check if container is running
docker-compose ps
```

### 3. Using the RAG System

#### Build the Index
```bash
# Execute the build_index.py script inside the container
docker-compose exec rag-system python rag/index/build_index.py
```

#### Ask Questions
```bash
# Run the ask.py script interactively
docker-compose exec rag-system python rag/index/ask.py
```

### 4. Alternative: Direct Docker Commands

If you prefer not to use docker-compose:

```bash
# Build the image
docker build -t omni-rag .

# Run with proxy environment variables
docker run -it --rm \
  -e HTTP_PROXY=http://your-proxy-server:port \
  -e HTTPS_PROXY=http://your-proxy-server:port \
  -e OPENAI_API_KEY=your-api-key \
  -v "$(pwd)/rag/data:/app/rag/data" \
  -v "$(pwd)/rag/index:/app/rag/index" \
  omni-rag python rag/index/build_index.py
```

### 5. Interactive Shell Access

To get a shell inside the container for debugging:

```bash
# Using docker-compose
docker-compose exec rag-system bash

# Using direct docker
docker run -it --rm omni-rag bash
```

### 6. Stopping the System

```bash
# Stop the container
docker-compose down

# Stop and remove volumes (if you want to start fresh)
docker-compose down -v
```

## Troubleshooting

### Proxy Issues
- Make sure your proxy URLs are correct in the `.env` file
- Some corporate proxies require authentication - you may need to add username/password to the proxy URL
- Test proxy connectivity: `docker-compose exec rag-system curl -I https://www.google.com`

### Permission Issues
- On Windows, make sure Docker Desktop has access to your project directory
- You might need to run PowerShell as Administrator

### Build Issues
- If the build fails, try: `docker-compose build --no-cache`
- Check Docker Desktop logs for detailed error messages

### Memory Issues
- The sentence-transformers model download might require significant memory
- Consider increasing Docker Desktop memory allocation in settings

## File Structure After Setup

```
omni-rag/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── requirements.txt
└── rag/
    ├── data/           # Your PDF files go here
    └── index/          # Generated index files
        ├── faiss.index
        └── meta.pkl
```

## Benefits of Docker Setup

1. **Consistent Environment**: Same Python version and dependencies across all machines
2. **Proxy Handling**: Environment variables are properly passed through
3. **Isolation**: No conflicts with your local Python installation
4. **Portability**: Easy to deploy on any machine with Docker
5. **Reproducible**: Exact same setup every time
