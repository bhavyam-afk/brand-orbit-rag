import json
from utils.pipeline import run_pipeline


def load_golden_data():
    with open("data/golden.json", "r") as f:
        return json.load(f)


def compute_metrics(retrieved_ids, relevant_ids):
    retrieved_set = set(retrieved_ids[:10])
    relevant_set = set(relevant_ids)

    tp = len(retrieved_set & relevant_set)

    precision = tp / 10.0 if 10 > 0 else 0
    recall = tp / len(relevant_set) if relevant_set else 0

    # MRR
    mrr = 0
    for rank, rid in enumerate(retrieved_ids[:10], start=1):
        if rid in relevant_set:
            mrr = 1.0 / rank
            break

    return precision, recall, mrr


def evaluate():
    golden_data = load_golden_data()

    total_precision = 0
    total_recall = 0
    total_mrr = 0
    num_queries = len(golden_data)

    for item in golden_data:
        query = item["query"]
        relevant_ids = item["relevant_ids"]

        try:
            result = run_pipeline(query)
            results = result.get("results", [])
            retrieved_ids = [int(item["id"]) for item in results if "id" in item]

            precision, recall, mrr = compute_metrics(retrieved_ids, relevant_ids)

            print(f"Query: {query}")
            print(f"  Precision@10: {precision:.3f}")
            print(f"  Recall@10: {recall:.3f}")
            print(f"  MRR: {mrr:.3f}")
            print(f"  Retrieved IDs: {retrieved_ids[:10]}")
            print(f"  Relevant IDs: {relevant_ids}")
            print()

            total_precision += precision
            total_recall += recall
            total_mrr += mrr

        except Exception as e:
            print(f"Error evaluating query '{query}': {e}")
            num_queries -= 1  # exclude from average

    if num_queries > 0:
        avg_precision = total_precision / num_queries
        avg_recall = total_recall / num_queries
        avg_mrr = total_mrr / num_queries

        print("Overall Metrics:")
        print(f"  Average Precision@10: {avg_precision:.3f}")
        print(f"  Average Recall@10: {avg_recall:.3f}")
        print(f"  Average MRR: {avg_mrr:.3f}")
    else:
        print("No queries evaluated successfully.")


if __name__ == "__main__":
    evaluate()