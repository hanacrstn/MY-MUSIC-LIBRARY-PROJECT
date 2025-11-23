import json
from typing import Any, Optional

class JsonStorage:
    @staticmethod
    def read(file_path: str, default: Optional[Any] = None) -> Any:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return default
        except json.JSONDecodeError:
            return default

    @staticmethod
    def write(file_path: str, data: Any) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as error:
            print(f"[ERROR] Unable to write data to {file_path}: {error}")