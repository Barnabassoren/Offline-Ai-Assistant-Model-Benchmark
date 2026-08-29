import ollama
import json
from pydantic import BaseModel, Field, ValidationError
from vectorstore import search_notes


class RevisionAnswer(BaseModel):
    question: str
    answer: str
    confidence: float = Field(ge=0, le=1)


def ask_question(query: str, top_k: int = 3, model: str = "llama3.2", max_retries: int = 3):
    # step 1: retrieval
    chunks = search_notes(query, top_k=top_k)

    context_text = ""
    for chunk in chunks:
        context_text += chunk["header_path"] + "\n" + chunk["text"] + "\n\n"

    # step 2: pehla message banao
    messages = [
        {
            "role": "user",
            "content": (
                f"Answer the question using ONLY the context below.\n\n"
                f"Context:\n{context_text}\n\n"
                f"Question: {query}"
            )
        }
    ]

    # step 3: retry loop
    for attempt in range(1, max_retries + 1):
        response = ollama.chat(
            model=model,
            messages=messages,
            format=RevisionAnswer.model_json_schema()
        )
        raw_content = response["message"]["content"]

        try:
            parsed_dict = json.loads(raw_content)
            validated = RevisionAnswer(**parsed_dict)
            return {"result": validated, "attempts": attempt}   # kaamyabi - turant return karo

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Attempt {attempt} fail hui: {e}")
            # model ko uska galat jawab aur error dikhao, retry ke liye
            messages.append({"role": "assistant", "content": raw_content})
            messages.append({
                "role": "user",
                "content": f"That was invalid: {e}. Please fix it and respond with valid JSON only."
            })

    return {"result": None, "attempts": max_retries}


# actual use
user_query = input("Apna sawaal pucho:")
outcome = ask_question(user_query)

if outcome["result"]:
    print("=== FINAL ANSWER ===")
    print("Question:", outcome["result"].question)
    print("Answer:", outcome["result"].answer)
    print("Confidence:", outcome["result"].confidence)
    print("Attempts needed:", outcome["attempts"])
else:
    print("Sab retries fail ho gayi")