import json

def load():
    try:
        with open("Storage.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File Storage.json not found. Returning an empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def save(data):
    try:
        with open("Storage.json", 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")

def save_queue(queue_data):
    """Save queue state to Queue_State.json"""
    try:
        with open("Queue_State.json", 'w') as file:
            json.dump(queue_data, file, indent=4)
    except Exception as e:
        print(f"Error saving queue state: {e}")

def load_queue():
    """Load queue state from Queue_State.json"""
    try:
        with open("Queue_State.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding queue state: {e}")
        return None