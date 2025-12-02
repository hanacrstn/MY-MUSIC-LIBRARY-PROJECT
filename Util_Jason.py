import json
import os
from datetime import datetime

def create_backup(filename):
    """Create a backup of the file before modifying it"""
    try:
        if os.path.exists(filename):
            backup_name = f"{filename}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(filename, 'r') as original:
                with open(backup_name, 'w') as backup:
                    backup.write(original.read())
            # Keep only the 3 most recent backups
            cleanup_old_backups(filename)
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

def cleanup_old_backups(filename, keep=3):
    """Keep only the most recent N backup files"""
    try:
        backups = [f for f in os.listdir('.') if f.startswith(f"{filename}.backup.")]
        backups.sort(reverse=True)
        for old_backup in backups[keep:]:
            os.remove(old_backup)
    except Exception:
        pass

def load():
    """Load data from Storage.json with error handling"""
    try:
        with open("Storage.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Validate structure
            if not isinstance(data, dict):
                print("Warning: Invalid data structure. Initializing empty data.")
                return {"Tracks": [], "Playlists": []}
            
            # Ensure required keys exist
            if "Tracks" not in data:
                data["Tracks"] = []
            if "Playlists" not in data:
                data["Playlists"] = []
            
            return data
            
    except FileNotFoundError:
        print(f"File Storage.json not found. Creating new file.")
        initial_data = {"Tracks": [], "Playlists": []}
        save(initial_data)
        return initial_data
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("The file may be corrupted. Check Storage.json.backup files.")
        return {"Tracks": [], "Playlists": []}
    
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        return {"Tracks": [], "Playlists": []}

def save(data):
    """Save data to Storage.json with backup and validation"""
    try:
        # Validate data structure before saving
        if not isinstance(data, dict):
            print("Error: Cannot save invalid data structure.")
            return False
        
        if "Tracks" not in data or "Playlists" not in data:
            print("Error: Data missing required keys (Tracks, Playlists).")
            return False
        
        # Create backup before saving
        create_backup("Storage.json")
        
        # Save with pretty formatting
        with open("Storage.json", 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        return True
        
    except IOError as e:
        print(f"Error saving to file: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error saving data: {e}")
        return False

def save_queue(queue_data):
    """Save queue state to Queue_State.json"""
    try:
        if queue_data is None:
            # Clear queue file
            with open("Queue_State.json", 'w', encoding='utf-8') as file:
                json.dump(None, file)
            return True
        
        # Validate queue data structure
        if not isinstance(queue_data, dict):
            print("Error: Invalid queue data structure.")
            return False
        
        required_keys = ["tracks", "current_index", "shuffle", "repeat", "playing"]
        if not all(key in queue_data for key in required_keys):
            print("Error: Queue data missing required keys.")
            return False
        
        with open("Queue_State.json", 'w', encoding='utf-8') as file:
            json.dump(queue_data, file, indent=4, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Error saving queue state: {e}")
        return False

def load_queue():
    """Load queue state from Queue_State.json"""
    try:
        with open("Queue_State.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # None means empty queue
            if data is None:
                return None
            
            # Validate structure
            if not isinstance(data, dict):
                print("Warning: Invalid queue state structure.")
                return None
            
            required_keys = ["tracks", "current_index", "shuffle", "repeat", "playing"]
            if not all(key in data for key in required_keys):
                print("Warning: Queue state missing required keys.")
                return None
            
            return data
            
    except FileNotFoundError:
        # No queue state file is normal for first run
        return None
    
    except json.JSONDecodeError as e:
        print(f"Error decoding queue state: {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected error loading queue state: {e}")
        return None

def verify_data_integrity():
    """Verify the integrity of Storage.json"""
    try:
        data = load()
        
        issues = []
        
        # Check for duplicate track IDs
        track_ids = [t.get("id") for t in data.get("Tracks", [])]
        if len(track_ids) != len(set(track_ids)):
            issues.append("Duplicate track IDs found")
        
        # Check for tracks with invalid durations
        for track in data.get("Tracks", []):
            if track.get("duration") == "invalid" or track.get("duration") is None:
                issues.append(f"Track '{track.get('title')}' has invalid duration")
        
        # Check playlist references
        all_track_ids = set(track_ids)
        for playlist in data.get("Playlists", []):
            for playlist_name, tracks in playlist.items():
                for track in tracks:
                    if track.get("id") not in all_track_ids:
                        issues.append(f"Playlist '{playlist_name}' references non-existent track ID {track.get('id')}")
        
        if issues:
            print("\n" + "!" * 60)
            print("DATA INTEGRITY ISSUES FOUND:".center(60))
            print("!" * 60)
            for issue in issues:
                print(f"  - {issue}")
            print("!" * 60 + "\n")
            return False
        
        return True
        
    except Exception as e:
        print(f"Error verifying data integrity: {e}")
        return False
