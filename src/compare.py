import time
from main import ask_question

def test_one_model(query: str, model: str):
    start_time = time.time()
    outcome = ask_question(query, model=model)
    elapsed_time = time.time() - start_time

    if outcome["result"]:
        return {
            "model": model,
            "answer": outcome["result"].answer,
            "confidence": outcome["result"].confidence,
            "attempts_needed": outcome["attempts"],
            "time_seconds": round(elapsed_time, 2)
        }
    else:
        return {
            "model": model,
            "answer": None,
            "confidence": None,
            "attempts_needed": outcome["attempts"],
            "time_seconds": round(elapsed_time, 2),
            "error": "Failed after all retries"
        }


if __name__ == "__main__":
    query = "What is Round Robin scheduling?"
    models_to_test = ["llama3.2", "phi3", "gemma2"]  

    all_results = []

    for model in models_to_test:
        print(f"\nTesting {model}...")
        result = test_one_model(query, model=model)
        all_results.append(result)

    print("\n\n=== COMPARISON TABLE ===\n")
    for r in all_results:
        print(f"--- {r['model']} ---")
        print("Answer:", r["answer"])
        print("Confidence:", r["confidence"])
        print("Time:", r["time_seconds"], "seconds")
        print("Attempts:", r["attempts_needed"])
        print()