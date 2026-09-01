def header_level(line: str) -> int:
    """Returns 0 if not a header, other wise header level (1 for # and 2 for ##)"""
    stripped = line.strip()
    level = 0       
    for char in stripped:
        if char == "#":
            level += 1
        else:
            break
    return level

def split_by_size_sliding_window(text: str, max_chunk_size: int = 100, overlap: int = 15) -> list[str]:
    words = text.split(" ")
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_chunk_size
        chunk_word = words[start: end]
        chunks.append(" ".join(chunk_word))
        start += max_chunk_size - overlap

    return chunks

def split_by_size(text:str, max_chunk_size:int = 20) -> list[str]:
    words = text.split(" ")
    chunks = []
    buffer = ""

    for word in words:
        if len(buffer) + len(word) > max_chunk_size:
            chunks.append(buffer.strip())
            buffer = ""
        buffer += word + " "

    if buffer.strip():
        chunks.append(buffer.strip())

    return chunks

# result = split_by_size("the quick brown fox jumps", max_chunk_size=20)
# for i, chunk in enumerate(result):
#     print(f"chunk {i}: '{chunk}' (length {len(chunk)})")

def chunk_markdown(text: str) -> list[dict]:
    lines = text.split("\n")
    sections = []
    current_section = []
    stack = []

    for line in lines:
        level = header_level(line)

        if level > 0:
            if current_section:
                sections.append({
                    "header_path": " > ".join(stack),
                    "text": "\n".join(current_section).strip()
                })
                current_section = []

            title = line.strip().lstrip("#").strip()
            stack = stack[:level - 1]
            stack.append(title)
            current_section.append(line)
        else:
            current_section.append(line)

    if current_section:
        sections.append({
            "header_path": " > ".join(stack),
            "text": "\n".join(current_section).strip()
        })

    return sections

def separate_code_blocks(text:str) -> list[dict]:
    parts = text.split("```")
    pieces = []

    for i, part in enumerate(parts):
        if part == "":
            continue #empty part skip it 

        if i % 2 == 0:
            pieces.append({
                "type": "text",
                "content": part
            })
        else:
            pieces.append({
                "type":"code",
                "content":"```" + part + "```"
            })

    return pieces

def apply_size_limit(sections: list[dict], max_chunk_size: int = 800) -> list[dict]:
    final_sections = []

    for section in sections:

        #we will break here into "text" and "code"
        pieces = separate_code_blocks(section["text"])

        for piece in pieces:
            #check if it is "text" or "code"
            if piece["type"] == "code":
                #this is code block so never break this section 
                final_sections.append({
                    "header_path": section["header_path"],
                    "text": piece["content"]
                })
            else:
                #this is text section so check its length
                if len(piece["content"]) <= max_chunk_size:
                    final_sections.append({
                        "header_path": section["header_path"],
                        "text": piece["content"]
                    })
                else:
                    #small_pieces = split_by_size(piece["content"], max_chunk_size)
                    small_pieces = split_by_size_sliding_window(piece["content"], max_chunk_size)

                    for small_piece in small_pieces:
                        final_sections.append({
                            "header_path":section["header_path"],
                            "text": small_piece
                        })

    return final_sections

with open("data/docs/os_scheduling.md", encoding="utf-8") as f:
    real_text = f.read()

sections = chunk_markdown(real_text)
final_sections = apply_size_limit(sections, max_chunk_size=300)  # small limit on purpose, to force some splitting

