from pypdf import PdfReader
from chunking import split_by_size_sliding_window

def extract_pdf_text(pdf_path: str) -> list[dict]:
    """Extract text from pdf, page-wise.
    Returns: [{"page_number": 1, "text":"..."}, {"page_number":2, "text":"..."}]"""

    reader = PdfReader(pdf_path)
    pages_data = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text.strip(): #skip empty page
            pages_data.append({
                "page_number": i+1,
                "text": text
            })

    return pages_data

def chunk_pdf(pdf_path, max_chunk_size: int = 500) -> list[dict]:
    """Extract text from pdf and i divide size based chunk here with page number"""
    pages_data = extract_pdf_text(pdf_path)
    final_chunks = []

    for page in pages_data:
        pieces = split_by_size_sliding_window(page["text"], max_chunk_size)

        for piece in pieces:
            final_chunks.append({
                "header_path": f"Page {page["page_number"]}",
                "text": piece
            })
    return final_chunks

if __name__ == "__main__":
    chunks = chunk_pdf("data/docs/computer_networks.pdf", max_chunk_size=90)

    print("Total chunks:", len(chunks))
    for i, c in enumerate(chunks):
        print(f"--- chunk {i} ---")
        print("header_path:", c["header_path"])
        print("length:", len(c["text"]))
        print(c["text"][:100])
        print()