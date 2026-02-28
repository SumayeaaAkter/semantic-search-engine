# Semantic Search Engine

## Overview

This project implements a lightweight semantic search pipeline that retrieves documents based on meaning rather than exact keyword matching. It begins by scraping and cleaning raw web content, storing structured text in DuckDB for efficient access and management. The system then generates dense vector embeddings using a pre-trained Transformer model from Hugging Face (SentenceTransformers) and indexes those embeddings in ChromaDB.

When a user submits a natural language query, the query is encoded into the same vector space as the stored documents. The system computes similarity scores between the query embedding and document embeddings, returning the most semantically relevant result. This demonstrates how modern embedding-based retrieval systems operate end to end.

## How It Works

The pipeline is organised into two main stages:

### 1. Data Ingestion
- Fetches and parses selected web pages  
- Removes unnecessary HTML elements (scripts, styles, navigation)  
- Cleans and normalises text content  
- Stores processed documents in a DuckDB database  

### 2. Embedding & Retrieval
- Loads documents from DuckDB  
- Generates dense vector embeddings using the `all-MiniLM-L6-v2` Transformer model  
- Stores embeddings and metadata in ChromaDB  
- Encodes user queries into the same embedding space  
- Computes similarity scores to identify the closest matching document  

Rather than relying on simple keyword overlap, the system compares semantic representations, allowing it to retrieve content based on contextual meaning.

## Tech Stack

- Python  
- DuckDB  
- Hugging Face SentenceTransformers  
- ChromaDB  
- BeautifulSoup  
- Requests  

## Usage

Run ingestion:

python ingest.py

Run embedding and semantic search:

python semantic_search.py

## What This Project Demonstrates

- End-to-end embedding-based retrieval system design  
- Practical application of Transformer models for semantic encoding  
- Lightweight data engineering using DuckDB  
- Vector similarity search with ChromaDB  
- Clear separation between ingestion and retrieval stages  
