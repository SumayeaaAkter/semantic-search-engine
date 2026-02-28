from chromadb import Client
from sentence_transformers import SentenceTransformer
import duckdb

DB_FILE = "sotonlm.duckdb"


def load_data_from_duckdb():
    query = """
        SELECT id, url, clean_text
        FROM training_corpus
        WHERE LENGTH(clean_text) > 200;
    """
    con = duckdb.connect(DB_FILE)
    return con.execute(query).fetchall()


def main():
    # Load documents from DuckDB
    print("Loading documents from DuckDB...")
    docs = load_data_from_duckdb()
    print(f"Loaded {len(docs)} documents.")

    if not docs:
        print("No documents found, exiting.")
        return

    #Load the embedding model
    print("Loading embedding model (this might take a bit the first time)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create embeddings for each document's clean_text
    print("Creating embeddings...")
    texts = [doc[2] for doc in docs]  # doc[2] = clean_text
    embeddings = model.encode(texts)
    print("Embeddings created. Shape:", embeddings.shape)

    # Set up Chroma vector database
    print("Setting up Chroma vector database...")
    chroma = Client()
    collection = chroma.get_or_create_collection(name="queen_workshop")

    # Add documents + embeddings into Chroma
    print("Adding documents to vector DB...")
    ids = [str(doc[0]) for doc in docs]           # use id as string
    metadatas = [{"url": doc[1]} for doc in docs]  # store URL as metadata

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Documents stored in Chroma.")

    # Run a semantic search query
    print("\nRunning semantic search...")
    #search_query = "I need a fast, column-oriented analytical database for local use."
    search_query = "What is the novel about the Bennet sisters about?"

    print("Search query:", search_query)

    results = collection.query(
        query_texts=[search_query],
        n_results=1
    )

    top_id = results["ids"][0][0]
    top_url = results["metadatas"][0][0]["url"]
    top_doc = results["documents"][0][0]
    top_distance = results["distances"][0][0]

    print("\nTop match:")
    print("  Document ID:", top_id)
    print("  URL:", top_url)
    print("  Distance (smaller = closer):", top_distance)
    print("  Snippet:", top_doc[:200], "...")


if __name__ == "__main__":
    main()
