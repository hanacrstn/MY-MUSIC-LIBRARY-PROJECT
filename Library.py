from Track import Track
from Util_Jason import load, save
from Duration import sec_to_min, total_duration
from Sorting import merge_sort
from Pagination import Pagination

class MusicLibrary:
    def __init__(self):
        self.data = load()
    
    def _track_exists(self, title, artist):
        """Check if track already exists in library"""
        return any(t["title"].lower().strip() == title.lower().strip() and 
                   t["artist"].lower().strip() == artist.lower().strip() 
                   for t in self.data.get("Tracks", []))
            
    def createTrack(self):
        title = input("Enter Track Title: ")
        artist = input("Enter Track Artist: ")
        featured_artist = input("Enter Featured Artist (or press Enter to skip): ")
        album = input("Enter Track Album: ")
        duration = input("Enter Track Duration (mm:ss): ")

        try:
            if "Tracks" not in self.data:
                self.data["Tracks"] = []

            if self._track_exists(title, artist):
                print("\n" + "!" * 60)
                print("ERROR: This track already exists in your library!".center(60))
                print(f"'{title}' by {artist}".center(60))
                print("!" * 60)
                print("\nCannot add duplicate tracks. Please try a different track.\n")
                return

            track_id = len(self.data["Tracks"]) + 1
            new_track = Track(track_id, title, artist, album, duration, featured_artist)
            if new_track.duration == "invalid":
                print("\n>> Failed to add track due to invalid input. Must be in mm:ss or in raw seconds.")
            else:
                self.data["Tracks"].append(new_track.to_dict())
                save(self.data)
                print("\nTrack Successfully Added to the Library!\n")

        except ValueError as e:
            print(f"Error adding track: {e}")

    def _paginated_display(self, tracks, title, selection_mode=False):
        """Generic paginated display for tracks"""
        if not tracks:
            print("No tracks found.")
            return None
        
        sorted_tracks = merge_sort(tracks, key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"{title} (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, track in enumerate(page_tracks, start=start_index):
                print(f"\t[{idx}]   {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            nav = "Enter track number to select | " if selection_mode else ""
            print(f"{nav}N → Next | P → Previous | Q → {'Cancel' if selection_mode else 'Back to Menu'}")
            print("-" * 60)
            
            choice = input("Choose: ").lower()
            
            if choice == 'n':
                if pagination.current_page < pagination.total_pages():
                    pagination.next_page()
                else:
                    print("Already at the last page.")
            elif choice == 'p':
                if pagination.current_page > 1:
                    pagination.previous_page()
                else:
                    print("Already at the first page.")
            elif choice == 'q':
                return None
            elif selection_mode:
                try:
                    selection = int(choice) - 1
                    if 0 <= selection < len(sorted_tracks):
                        return sorted_tracks[selection]
                    print("Invalid track number.")
                except ValueError:
                    print("Invalid input. Enter a number or N/P/Q.")

    def displayTracks(self):
        self._paginated_display(self.data.get("Tracks", []), "Tracks")

    def displayTracksForSelection(self):
        return self._paginated_display(self.data.get("Tracks", []), "Select a Track", selection_mode=True)

    def getTotalDuration(self):
        return total_duration(self.data, "Tracks")

    def deleteTrack(self):
        """Delete a track from the library"""
        tracks = self.data.get("Tracks", [])
        if not tracks:
            print("\nNo tracks available to delete.")
            return None
        
        sorted_tracks = merge_sort(tracks, key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"Delete Track (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, track in enumerate(page_tracks, start=start_index):
                print(f"\t[{idx}]   {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            print("Enter track number to delete | N → Next | P → Previous | Q → Cancel")
            print("-" * 60)
            
            choice = input("Choose: ").lower()
            
            if choice == 'n':
                if pagination.current_page < pagination.total_pages():
                    pagination.next_page()
                else:
                    print("Already at the last page.")
            elif choice == 'p':
                if pagination.current_page > 1:
                    pagination.previous_page()
                else:
                    print("Already at the first page.")
            elif choice == 'q':
                return None
            else:
                try:
                    selection = int(choice) - 1
                    if 0 <= selection < len(sorted_tracks):
                        track_to_delete = sorted_tracks[selection]
                        confirm = input(f"\nDelete '{track_to_delete['title']}' by {track_to_delete['artist']}? (y/n): ").lower()
                        
                        if confirm == 'y':
                            self.data["Tracks"].remove(track_to_delete)
                            
                            # Remove from all playlists
                            if "Playlists" in self.data:
                                for playlist in self.data["Playlists"]:
                                    for tracks in playlist.values():
                                        if track_to_delete in tracks:
                                            tracks.remove(track_to_delete)
                            
                            save(self.data)
                            print(f"\nTrack '{track_to_delete['title']}' deleted successfully!")
                            print("(Also removed from all playlists)")
                            return track_to_delete
                        else:
                            print("\nDeletion cancelled.")
                            return None
                    else:
                        print("Invalid track number.")
                except ValueError:
                    print("Invalid input. Enter a number or N/P/Q.")
