import requests
from bs4 import BeautifulSoup
import duckdb
from datetime import datetime
import os

DB_FILE = 'sotonlm.duckdb'

URLS_TO_SCRAPE = [
    "https://docs.python.org/3/library/random.html",
    "https://www.gutenberg.org/files/1342/1342-h/1342-h.htm",
    "https://duckdb.org/docs/sql/introduction",
    "https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request"
]

def fetch_and_clean_text(url: str) -> str:
    try:
        print(f"-> Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        clean_text = soup.get_text(separator=' ', strip=True)
        
        if len(clean_text) < 100:
            print(f"   [WARN] Low quality text. Skipping.")
            return ""
            
        return clean_text
        
    except requests.exceptions.RequestException as e:
        print(f"-> [ERROR] Failed to fetch {url}. Error: {e}")
        return ""

def setup_and_populate_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Existing database '{DB_FILE}' removed.")
        
    conn = duckdb.connect(database=DB_FILE)

    conn.execute("""
        CREATE TABLE training_corpus (
            id INTEGER,
            url VARCHAR,
            clean_text VARCHAR,
            ingest_timestamp TIMESTAMP
        );
    """)
    print(f"Created table 'training_corpus' in '{DB_FILE}'.")
    
    records_inserted = 0
    
    for idx, url in enumerate(URLS_TO_SCRAPE):
        clean_content = fetch_and_clean_text(url)
        
        if clean_content:
            conn.execute("INSERT INTO training_corpus VALUES (?, ?, ?, ?)", (idx + 1, url, clean_content, datetime.now()))
            records_inserted += 1
            
    conn.close()
    print(f"\n--- SETUP COMPLETE ---")
    print(f"DuckDB file '{DB_FILE}' is ready.")
    print(f"Total {records_inserted} clean documents inserted.")
    
if __name__ == "__main__":
    setup_and_populate_db()