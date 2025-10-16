import os, json, pickle, glob, math
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from PyPDF2 import PdfReader

INDEX_DIR = Path("index")
DATA_DIR = Path("../data")  # Go up one level from index/ to data/

def load_text(fp: Path) -> str:
    if fp.suffix.lower() == ".pdf":
        reader = PdfReader(str(fp))
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    else:
        return fp.read_text(encoding="utf-8", errors="ignore")

def chunk_text(text: str, target_chars=3500, overlap=400) -> List[str]:
    text = " ".join(text.split())  # collapse whitespace
    chunks = []
    i = 0
    while i < len(text):
        j = min(i + target_chars, len(text))
        # hard cut at whitespace if possible
        if j < len(text):
            k = text.rfind(" ", i, j)
            if k != -1 and k - i > target_chars * 0.6:
                j = k
        chunks.append(text[i:j].strip())
        i = max(j - overlap, j)
    return [c for c in chunks if c]

def main():
    try:
        INDEX_DIR.mkdir(exist_ok=True, parents=True)
        files = [Path(p) for p in glob.glob(str(DATA_DIR / "**/*"), recursive=True)
                 if Path(p).is_file() and Path(p).suffix.lower() in {".pdf",".txt",".md"}]
        if not files:
            print(f"No source files found in {DATA_DIR}")
            input("Press Enter to continue...")
            return

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        texts, metas = [], []
        for fp in files:
            t = load_text(fp)
            if not t.strip():
                continue
            for idx, ch in enumerate(chunk_text(t)):
                texts.append(ch)
                metas.append({"source": str(fp), "chunk_id": idx, "title": fp.name})

        print(f"Chunks: {len(texts)}")
        emb = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
        emb = np.asarray(emb, dtype="float32")

        dim = emb.shape[1]
        index = faiss.IndexFlatIP(dim)  # cosine if vectors are normalized
        index.add(emb)

        faiss.write_index(index, str(INDEX_DIR / "faiss.index"))
        with open(INDEX_DIR / "meta.pkl", "wb") as f:
            pickle.dump({"metas": metas, "texts": texts}, f)

        print("Index built -> ./index/faiss.index and ./index/meta.pkl")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
