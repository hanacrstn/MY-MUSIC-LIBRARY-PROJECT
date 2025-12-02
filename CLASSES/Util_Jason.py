import json

def load():
    try:
        with open("Store.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {"Store.json"} not found. Returning an empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def save(data):
    try:
        with open("Store.json", 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")
