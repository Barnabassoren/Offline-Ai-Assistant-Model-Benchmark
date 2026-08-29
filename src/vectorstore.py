import chromadb
from sentence_transformers import SentenceTransformer
from chunking import chunk_markdown, apply_size_limit
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("college_notes")


def search_notes(query: str, top_k: int = 2) -> list[dict]:
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "header_path": results["metadatas"][0][i]["header_path"],
            "text": results["documents"][0][i]
        })

    return chunks


if __name__ == "__main__":
    folder_path = "data/docs"
    files = os.listdir(folder_path)

    all_chunks = []

    for filename in files:
        full_path = os.path.join(folder_path, filename)

        with open(full_path, encoding="utf-8") as f:
            text = f.read()

        sections = chunk_markdown(text)
        file_chunks = apply_size_limit(sections, max_chunk_size=300)

        for chunk in file_chunks:
            chunk["source_file"] = filename
            all_chunks.append(chunk)

    print("Total chunks sabhi files se:", len(all_chunks))

    texts_to_embed = []
    for chunk in all_chunks:
        combined = chunk["header_path"] + "\n" + chunk["text"]
        texts_to_embed.append(combined)

    embeddings = model.encode(texts_to_embed)

    ids = []
    for i, chunk in enumerate(all_chunks):
        ids.append(f"{chunk['source_file']}_chunk_{i}")

    metadatas = []
    for chunk in all_chunks:
        metadatas.append({
            "header_path": chunk["header_path"],
            "source_file": chunk["source_file"]
        })

    documents = []
    for chunk in all_chunks:
        documents.append(chunk["text"])

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        documents=documents
    )

    print("Store ho gaya! Total items collection mein:", collection.count())