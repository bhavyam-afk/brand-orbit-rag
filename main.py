import json
from utils.pipeline import run_pipeline


def print_influencer_details(results):
    for idx, item in enumerate(results, start=1):
        influencer = item.get("influencer", {})
        print(f"\nResult #{idx}")
        print("------------------------------")
        print(f"ID: {item.get('id')}")
        print(f"Hybrid score: {item.get('score')}")
        if item.get("llm_score") is not None:
            print(f"LLM rerank score: {item.get('llm_score')}")
        print("Influencer details:")
        print(json.dumps(influencer, indent=2, ensure_ascii=False))


def main():
    query = "funny influencers wit good engament"
    result = run_pipeline(query)

    print("Original query:", result.get("original_query"))
    print("Final query:", result.get("final_query"))

    results = result.get("results")
    if isinstance(results, list):
        print("Number of results:", len(results))
        if results:
            print_influencer_details(results)
    else:
        print("Results is not a list, actual value:", results)


if __name__ == "__main__":
    main()
