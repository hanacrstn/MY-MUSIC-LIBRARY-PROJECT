import json
from Track import track, duration

class Playlist:
    def __init__(self, name):
        self.__name = name
        self.__tracks = []

    def addTrack(self, track_obj):
        self.__tracks.append(track_obj)

    def removeTrack(self, title):
        self.__tracks = [t for t in self.__tracks if t.title != title]

    def getTracks(self):
        return self.__tracks.copy()

    def getName(self):
        return self.__name

    def store_dict(self):
        result = []
        for t in self.__tracks:
            result.append({
                "title": t.title,
                "artist": t.artist,
                "album": t.album,
                "additional_artist": t.additional_artist,
                "duration": t.get_duration() if isinstance(t, duration) else None
            })
        return result

    @classmethod
    def fetch_dict(cls, name, track_list):
        playlist = cls(name)
        for t in track_list:
            if t.get("duration"):
                track_obj = duration(
                    t["title"],
                    t["artist"],
                    t["album"],
                    t.get("additional_artist", []),
                    t["duration"]
                )
            else:
                track_obj = track(
                    t["title"],
                    t["artist"],
                    t["album"],
                    t.get("additional_artist", [])
                )
            playlist.addTrack(track_obj)
        return playlist

class PlaylistManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.playlists = {}
        self.load_from_json()

    def load_from_json(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)
        for playlist_obj in data.get("Playlists", []):
            for name, tracks in playlist_obj.items():
                self.playlists[name] = Playlist.fetch_dict(name, tracks)

    def view_playlists(self):
        return list(self.playlists.keys())

    def view_tracks_in_playlist(self, playlist_name):
        if playlist_name not in self.playlists:
            return []
        tracks_info = []
        for t in self.playlists[playlist_name].getTracks():
            feat = f"(ft. {', '.join(t.additional_artist)})" if t.additional_artist else ""
            duration_str = t.get_duration() if isinstance(t, duration) else ""
            tracks_info.append(f"{t.title} - {t.artist}{feat} ({t.album}) [{duration_str}]")
        return tracks_info

    def create_playlist(self, name):
        if name in self.playlists:
            return False
        self.playlists[name] = Playlist(name)
        return True

    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]
            return True
        return False

    def add_track_to_playlist(self, playlist_name, track_obj):
        if playlist_name in self.playlists:
            self.playlists[playlist_name].addTrack(track_obj)
            return True
        return False

    def save_to_json(self):
        data = {"Playlists": []}
        for name, playlist in self.playlists.items():
            data["Playlists"].append({name: playlist.store_dict()})
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

def main():
    file_path = r"C:\Users\MACHENIKE\OneDrive\Desktop\DSA_FinalProject\store.json"
    manager = PlaylistManager(file_path)

    while True:
        print("\n--- Playlist Manager ---")
        print("1. View all playlists")
        print("2. View tracks in a playlist")
        print("3. Create a new playlist")
        print("4. Delete a playlist")
        print("5. Add a track to a playlist")
        print("6. Save and exit")

        choice = input("Choose an option: ")

        if choice == "1":
            playlists = manager.view_playlists()
            print("\nExisting Playlists:")
            for p in playlists:
                print("-", p)

        elif choice == "2":
            name = input("Enter playlist name: ")
            tracks = manager.view_tracks_in_playlist(name)
            if not tracks:
                print("Playlist not found or empty.")
            else:
                print(f"\nTracks in '{name}':")
                for t in tracks:
                    print("-", t)

        elif choice == "3":
            name = input("Enter new playlist name: ")
            if manager.create_playlist(name):
                print(f"Playlist '{name}' created.")
            else:
                print("Playlist already exists.")

        elif choice == "4":
            name = input("Enter playlist name to delete: ")
            if manager.delete_playlist(name):
                print(f"Playlist '{name}' deleted.")
            else:
                print("Playlist not found.")

        elif choice == "5":
            playlist_name = input("Enter playlist name to add track: ")
            title = input("Track title: ")
            artist = input("Artist: ")
            album = input("Album: ")
            add_artist = []
            if input("Add additional artists? (y/n): ").lower() == "y":
                add_artist = input("Enter additional artists (comma separated): ").split(",")
                add_artist = [a.strip() for a in add_artist]
            dur = input("Duration (mm:ss): ")
            track_obj = duration(title, artist, album, add_artist, dur)
            manager.add_track_to_playlist(playlist_name, track_obj)
            print("Track added.")

        elif choice == "6":
            manager.save_to_json()
            print("All changes saved. Exiting...")
            break

        else:
            print("Invalid choice. Try again.")
