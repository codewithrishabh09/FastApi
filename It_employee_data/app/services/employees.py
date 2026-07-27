import json
from pathlib import Path
from typing import List, Dict

data_file = Path(__file__).resolve().parent.parent.parent / "data" / "employees.json"

def load_data() -> List[Dict]:
    if not data_file.exists():
        raise FileNotFoundError(f"Product fil not fond at {data_file}")
    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)

def get_all_data() -> List[Dict]:
    return load_data()

def save_employee_data(Employee: List[Dict]) -> None:
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(employee,f, indent=2, ensure_ascii=False)