import json
from typing import Any

def read_json(file_path: str) -> Any:
    """Read and parse JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_json(file_path: str, data: Any) -> None:
    """Write data to JSON file with pretty formatting."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)