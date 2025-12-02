from Track import Track
from Util_Jason import load, save
from Duration import sec_to_min, total_duration
from Sorting import merge_sort
from Pagination import Pagination

class MusicLibrary:
    def __init__(self) -> None:
        self.data = load()
            
    def createTrack(self):
        title = input("Enter Track Title: ")
        artist = input("Enter Track Artist: ")
        featured_artist = input("Enter Featured Artist (or press Enter to skip): ")
        album = input("Enter Track Album: ")
        duration = input("Enter Track Duration (mm:ss): ")

        try:
            if "Tracks" not in self.data:
                self.data["Tracks"] = []

            # Check for duplicate tracks (same title and artist)
            for existing_track in self.data["Tracks"]:
                if (existing_track["title"].lower().strip() == title.lower().strip() and 
                    existing_track["artist"].lower().strip() == artist.lower().strip()):
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
                print ("\nTrack Successfully Added to the Library!\n")

        except ValueError as e:
            print(f"Error adding track: {e}")

    def displayTracks(self):
        if "Tracks" not in self.data or not self.data["Tracks"]:
            print("No tracks found.")
            return
        
        sorted_tracks = merge_sort(self.data["Tracks"], key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"Tracks (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, track in enumerate(page_tracks, start=start_index):
                print(f"\t[{idx}]   {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            print("N → Next Page | P → Previous Page | Q → Back to Menu")
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
                break
            else:
                print("Invalid option.")

    def displayTracksForSelection(self):
        """Display tracks with pagination for selection (returns selected track)"""
        if "Tracks" not in self.data or not self.data["Tracks"]:
            print("No tracks found.")
            return None
        
        sorted_tracks = merge_sort(self.data["Tracks"], key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"Select a Track (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, track in enumerate(page_tracks, start=start_index):
                print(f"\t[{idx}]   {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            print("Enter track number to select | N → Next | P → Previous | Q → Cancel")
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
                        return sorted_tracks[selection]
                    else:
                        print("Invalid track number.")
                except ValueError:
                    print("Invalid input. Enter a number or N/P/Q.")

    def getTotalDuration(self):
        """Get total duration of all tracks"""
        return total_duration(self.data, "Tracks")

    def deleteTrack(self):
        """Delete a track from the library"""
        if "Tracks" not in self.data or not self.data["Tracks"]:
            print("\nNo tracks available to delete.")
            return None
        
        sorted_tracks = merge_sort(self.data["Tracks"], key="title")
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
                            # Remove from main library
                            self.data["Tracks"].remove(track_to_delete)
                            
                            # Remove from all playlists
                            if "Playlists" in self.data:
                                for playlist in self.data["Playlists"]:
                                    for playlist_name, tracks in playlist.items():
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
