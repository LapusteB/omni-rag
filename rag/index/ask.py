import os, pickle
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

INDEX_DIR = Path("index")
load_dotenv()
console = Console()

def load_index():
    index = faiss.read_index(str(INDEX_DIR / "faiss.index"))
    with open(INDEX_DIR / "meta.pkl","rb") as f:
        payload = pickle.load(f)
    return index, payload["texts"], payload["metas"]

def retrieve(query, k=8):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    q = model.encode([query], normalize_embeddings=True)
    D, I = index.search(np.asarray(q, dtype="float32"), k)
    items = []
    for rank, idx in enumerate(I[0]):
        items.append((rank, texts[idx], metas[idx], float(D[0][rank])))
    return items

def compose_prompt(query, contexts):
    blocks = []
    for r, txt, meta, score in contexts:
        blocks.append(f"### Source {r+1}\n(Source: {meta['title']} | Path: {meta['source']} | Score: {score:.3f})\n{txt}\n")
    context = "\n\n".join(blocks)
    system = (
        "You are a precise assistant. Answer ONLY from the provided Sources.\n"
        "Cite sources inline like [S1], [S2] where S# matches Source #.\n"
        "If the context is insufficient, say 'Insufficient evidence.'"
    )
    user = f"Question: {query}\n\nSources:\n{context}\n\nAnswer with citations."
    return system, user

if __name__ == "__main__":
    try:
        if not (INDEX_DIR / "faiss.index").exists():
            print("No index found. Run: python build_index.py")
            input("Press Enter to continue...")
            exit(1)

        index, texts, metas = load_index()
        query = input("Ask: ").strip()
        
        if not query:
            print("No query provided.")
            input("Press Enter to continue...")
            exit(1)
            
        contexts = retrieve(query, k=8)
        system, user = compose_prompt(query, contexts)

        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=0.2
        )
        answer = resp.choices[0].message.content
        console.rule("[bold]Answer")
        console.print(Markdown(answer))
        console.rule("Sources")
        for r, _, meta, score in contexts:
            console.print(f"[S{r+1}] {meta['title']}  ({meta['source']})  score={score:.3f}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to continue...")
