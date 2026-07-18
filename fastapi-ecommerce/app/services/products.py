import json
from pathlib import Path
from typing import List, Dict

# products.py -> services/ -> app/ -> fastapi-ecommerce/ -> data/products.json
data_file = Path(__file__).resolve().parent.parent.parent / "data" / "dummy.json"


# load products when user refersh the page then load the fresh & updated data
def load_products() -> List[Dict]:
    if not data_file.exists():
        raise FileNotFoundError(f"Products file not found at {data_file}")
    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)

# get all the products when user call the products the show all products
def get_all_products() -> List[Dict]:
    return load_products()

# save all the products when user update & delete the data this routes is save data
def save_product(product:List[Dict]) -> None:
    with open (data_file, "w", encoding="utf-8") as f:
        json.dump(product,f, indent=2, ensure_ascii=False)

def add_product(product:Dict) -> Dict:
    products = get_all_products()

    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("sku already exixt")
    products.append(product)
    save_product(products)
    return product