#!/bin/bash

# RAG System Docker Helper Script

case "$1" in
    "build")
        echo "Building Docker image..."
        docker-compose build
        ;;
    "start")
        echo "Starting RAG system..."
        docker-compose up -d
        ;;
    "stop")
        echo "Stopping RAG system..."
        docker-compose down
        ;;
    "index")
        echo "Building index..."
        docker-compose exec rag-system python rag/index/build_index.py
        ;;
    "ask")
        echo "Starting interactive Q&A session..."
        docker-compose exec rag-system python rag/index/ask.py
        ;;
    "shell")
        echo "Opening shell in container..."
        docker-compose exec rag-system bash
        ;;
    "logs")
        echo "Showing container logs..."
        docker-compose logs rag-system
        ;;
    "status")
        echo "Container status:"
        docker-compose ps
        ;;
    *)
        echo "Usage: $0 {build|start|stop|index|ask|shell|logs|status}"
        echo ""
        echo "Commands:"
        echo "  build   - Build the Docker image"
        echo "  start   - Start the container"
        echo "  stop    - Stop the container"
        echo "  index   - Build the search index"
        echo "  ask     - Start interactive Q&A"
        echo "  shell   - Open shell in container"
        echo "  logs    - Show container logs"
        echo "  status  - Show container status"
        exit 1
        ;;
esac
