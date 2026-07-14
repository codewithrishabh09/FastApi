import json
from pathlib import Path
from typing import List, Dict

# products.py -> services/ -> app/ -> fastapi-ecommerce/ -> data/products.json
data_file = Path(__file__).resolve().parent.parent.parent / "data" / "product.json"

def load_products() -> List[Dict]:
    if not data_file.exists():
        raise FileNotFoundError(f"Products file not found at {data_file}")
    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)

def all_get_products() -> List[Dict]:
    return load_products()