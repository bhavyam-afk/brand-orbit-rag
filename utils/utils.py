from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent

def load_stopwords() -> list:
    stopwords_path = ROOT_DIR / 'data' / 'stopwords.txt'
    with open(stopwords_path, 'r') as f:
        return f.read().splitlines()

def load_influencers() -> list[dict]:
    influencers_path = ROOT_DIR / 'data' / 'influencers_data.json'
    with open(influencers_path, 'r') as f:
        return json.load(f)
