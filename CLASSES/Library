
from Track import Track
from json_utilz import load, save
from Duration import sec_to_min
from sort import merge_sort


class MusicLibrary:
    def __init__(self) -> None:
        self.data = load()
            
    def createTrack(self):
        title = input("Enter Track Title: ")
        artist = input("Enter Track Artist: ")
        album = input("Enter Track Album: ")
        duration = input("Enter Track Duration (mm:ss): ")

        try:
            if "Tracks" not in self.data:
                self.data["Tracks"] = []

            track_id = len(self.data["Tracks"]) + 1  
            new_track = Track(track_id, title, artist, album, duration)
            if new_track.getDuration() == "invalid":
                print("\n>> Failed to add track due to invalid input. Must be in mm:ss or in raw seconds.")
            else:
                self.data["Tracks"].append(new_track.to_dict())
                save(self.data)
                print ("\nTrack Successfully Added to the Library!\n")

        except ValueError as e:
            print(f"Error adding track: {e}")


    def displayTracks(self):
        if "Tracks" not in self.data or not self.data["Tracks"]:
            print("No tracks found.")
            return
        
        print("\nTracks:")
        track_counter = 1
        
        sorted_tracks = merge_sort(self.data["Tracks"], key="title")
        for track in sorted_tracks:
            print(f"\t[{track_counter}]   {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
            track_counter += 1
        
