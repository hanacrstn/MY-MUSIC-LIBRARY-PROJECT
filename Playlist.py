from Track import Track
from Util_Jason import load, save  
from Duration import total_duration, sec_to_min
from Sorting import merge_sort
from Pagination import Pagination

class Playlist:
    def __init__(self):
        self.data = load()
        self.list = []

    def updatePlaylistList(self):
        self.list = []
        if "Playlists" in self.data:
            for playlist in self.data["Playlists"]:
                for name in playlist:
                    self.list.append(name)

    def _track_exists_in_playlist(self, track, playlist_tracks):
        """Helper method to check if track exists in playlist"""
        for existing_track in playlist_tracks:
            if (existing_track["id"] == track["id"] or 
                (existing_track["title"].lower() == track["title"].lower() and 
                 existing_track["artist"].lower() == track["artist"].lower())):
                return True
        return False

    def _find_playlist_tracks(self, playlist_name):
        """Helper method to find playlist tracks by name"""
        for playlist in self.data["Playlists"]:
            if playlist_name in playlist:
                return playlist[playlist_name]
        return None

    def createPlaylist(self):
        while True:
            playlistName = input("Enter Playlist Name: ").strip()
            
            if not playlistName:
                print("\nPlaylist name cannot be empty. Please try again.\n")
                continue
            
            try:
                if "Playlists" not in self.data:
                    self.data["Playlists"] = []

                # Check for duplicate playlist names (case-insensitive)
                for playlist in self.data["Playlists"]:
                    for existing_name in playlist.keys():
                        if existing_name.lower() == playlistName.lower():
                            print("\n" + "!" * 60)
                            print("ERROR: Playlist name already exists!".center(60))
                            print(f"'{existing_name}' is already in your collection.".center(60))
                            print("!" * 60)
                            print("\nPlease choose a different name.\n")
                            break
                    else:
                        continue
                    break

                else:  
                    self.data["Playlists"].append({playlistName: []})
                    save(self.data) 
                    print("\n" + "=" * 60)
                    print("✓ Playlist added successfully!".center(60))
                    print(f"'{playlistName}' created.".center(60))
                    print("=" * 60 + "\n")
                    
                    self.updatePlaylistList() 
                    break  

            except Exception as e:
                print(f"Error adding playlist: {e}")

    def displayTracks(self, playlist_index):
        self.updatePlaylistList()
        try:
            playlist_index = int(playlist_index) - 1
            playlist_name = self.list[playlist_index]

            playlist_tracks = self._find_playlist_tracks(playlist_name)
            if playlist_tracks is None:
                print("\nPlaylist not found.")
                return

            if not playlist_tracks:
                print("\nNo tracks found in this playlist.")
                return

            sorted_tracks = merge_sort(playlist_tracks, key="title")
            pagination = Pagination(sorted_tracks, items_per_page=10)

            while True:
                print("\n" + "=" * 60)
                print(f"Playlist: '{playlist_name}' (Page {pagination.current_page}/{pagination.total_pages()})")
                
                # Calculate total duration for this playlist
                total_secs = sum(int(t.get("duration", 0)) for t in playlist_tracks)
                from Duration import format_duration
                print(f"Total duration: {format_duration(total_secs)}")
                print("=" * 60)

                page_tracks = pagination.get_page_items(pagination.current_page)
                start_index = pagination.start() + 1

                for idx, track in enumerate(page_tracks, start=start_index):
                    feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                    print(f"\t{idx}. {track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})")

                print("\n" + "-" * 60)
                print("N → Next Page | P → Previous Page | Q → Back")
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
            return

        except (ValueError, IndexError):
            print("\nInvalid input. Please enter a valid playlist number.")
    
    def displayPlaylists(self, with_pagination=False):
        self.updatePlaylistList()
        if not self.list:
            print("There are no Playlists made!")
            return
        
        if not with_pagination:
            # Simple display without pagination
            counter = 1
            for playlist_name in self.list:
                print(f"    [{counter}] {playlist_name}")
                counter += 1
        else:
            # Display with pagination
            pagination = Pagination(self.list, items_per_page=10)
            
            while True:
                print("\n" + "=" * 60)
                print(f"Available Playlists (Page {pagination.current_page}/{pagination.total_pages()})")
                print("=" * 60)
                
                page_playlists = pagination.get_page_items(pagination.current_page)
                start_index = pagination.start() + 1
                
                for idx, playlist_name in enumerate(page_playlists, start=start_index):
                    print(f"    [{idx}] {playlist_name}")
                
                print("\n" + "-" * 60)
                print("N → Next Page | P → Previous Page | Q → Back")
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

    def searchTrack(self, track):
        self.data = load()

        tracks = self.data.get("Tracks", [])
        if not tracks:
            print("\nNo tracks available in the music library.")
            return None

        track_lower = track.lower()
        results = [
            track for track in tracks
            if track_lower in track["title"].lower()
            or track_lower in track["artist"].lower()
            or track_lower in track["album"].lower()
        ]

        if not results:
            return []

        pagination = Pagination(results, items_per_page=10)

        while True:
            print("\n" + "=" * 60)
            print(f"Search Results (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)

            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1

            for idx, track in enumerate(page_tracks, start=start_index):
                feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                print(f"    [{idx}] {track['title']}{feat} by {track['artist']} ({track['duration']})")

            print("\n" + "-" * 60)
            print("N → Next Page | P → Previous Page | Q → Continue | C → Cancel")
            print("-" * 60)

            choice = input("Choose: ").lower().strip()

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
            elif choice == 'c':
                print("\nSearch cancelled.")
                return None
            elif not choice:
                print("Invalid option. Please enter a valid choice.")
            else:
                print("Invalid option.")

        return results

    def searchedTracks(self, option, playlist_name, matching_tracks):
        playlist_tracks = self._find_playlist_tracks(playlist_name)
        if playlist_tracks is None:
            print("\nPlaylist not found.")
            return False

        if option == 1:
            try:
                track_input = input("\nSelect a track to add (Enter number or 0 to cancel): ").strip()
                
                if not track_input:
                    print("\nInvalid input. Please enter a valid number.")
                    return False
                
                track_index = int(track_input)
                
                if track_index == 0:
                    print("\nOperation cancelled.")
                    return False
                
                track_index -= 1
                if track_index < 0 or track_index >= len(matching_tracks):
                    print("\nInvalid track selection.")
                    return False

                selected_track = matching_tracks[track_index]

                if self._track_exists_in_playlist(selected_track, playlist_tracks):
                    print("\n" + "!" * 60)
                    print("ERROR: Track already in playlist!".center(60))
                    print(f"'{selected_track['title']}' is already in '{playlist_name}'.".center(60))
                    print("!" * 60 + "\n")
                else:
                    playlist_tracks.append(selected_track)
                    save(self.data)
                    print(f"\n✓ Track '{selected_track['title']}' added to playlist '{playlist_name}'.")
                return True
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                return False

        elif option == 2:
            added_count = 0
            skipped_count = 0
            for selected_track in matching_tracks:
                if not self._track_exists_in_playlist(selected_track, playlist_tracks):
                    playlist_tracks.append(selected_track)
                    added_count += 1
                else:
                    skipped_count += 1

            if added_count > 0:
                save(self.data)
                print("\n" + "=" * 60)
                print(f"✓ {added_count} track(s) added to '{playlist_name}'".center(60))
                if skipped_count > 0:
                    print(f"{skipped_count} duplicate(s) skipped".center(60))
                print("=" * 60 + "\n")
            else:
                print("\n" + "!" * 60)
                print("No new tracks added".center(60))
                print("All selected tracks already exist in the playlist.".center(60))
                print("!" * 60 + "\n")
            return True
        
        elif option == 0:
            print("\nOperation cancelled.")
            return False
        else:
            print("\nInvalid option selected.")
            return False

    def displayTracksForSelection(self):
        """Display all tracks with pagination for selection"""
        self.data = load()
        tracks = self.data.get("Tracks", [])
        
        if not tracks:
            print("\nNo tracks available.")
            return None

        sorted_tracks = merge_sort(tracks, key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)

        while True:
            print("\n" + "=" * 60)
            print(f"Select a Track (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)

            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1

            for idx, track in enumerate(page_tracks, start=start_index):
                feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                print(f"\t[{idx}]   {track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})")

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

    def addTrack(self, playlist_name):
        selected_track = self.displayTracksForSelection()
        
        if selected_track is None:
            print("\nTrack addition cancelled.")
            return

        playlist_tracks = self._find_playlist_tracks(playlist_name)
        if playlist_tracks is None:
            print("\nPlaylist not found.")
            return

        if self._track_exists_in_playlist(selected_track, playlist_tracks):
            print("\n" + "!" * 60)
            print("ERROR: Track already in playlist!".center(60))
            print(f"'{selected_track['title']}' by {selected_track['artist']}".center(60))
            print(f"is already in '{playlist_name}'.".center(60))
            print("!" * 60 + "\n")
        else:
            playlist_tracks.append(selected_track)
            save(self.data)
            print("\n" + "=" * 60)
            print("✓ Track added successfully!".center(60))
            print(f"'{selected_track['title']}' → '{playlist_name}'".center(60))
            print("=" * 60 + "\n")
        return

    def removeTrackFromPlaylist(self, playlist_name):
        """Remove a track from a specific playlist"""
        playlist_tracks = self._find_playlist_tracks(playlist_name)
        if playlist_tracks is None:
            print("\nPlaylist not found.")
            return
        
        if not playlist_tracks:
            print("\nThis playlist has no tracks to remove.")
            return
        
        sorted_tracks = merge_sort(playlist_tracks, key="title")
        pagination = Pagination(sorted_tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"Remove Track from '{playlist_name}' (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, track in enumerate(page_tracks, start=start_index):
                feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                print(f"\t[{idx}] {track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            print("Enter track number to remove | N → Next | P → Previous | Q → Cancel")
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
                return
            else:
                try:
                    selection = int(choice) - 1
                    if 0 <= selection < len(sorted_tracks):
                        track_to_remove = sorted_tracks[selection]
                        confirm = input(f"\nRemove '{track_to_remove['title']}'? (y/n): ").lower()
                        if confirm == 'y':
                            playlist_tracks.remove(track_to_remove)
                            save(self.data)
                            print(f"\nTrack '{track_to_remove['title']}' removed from playlist '{playlist_name}'.")
                            return
                        else:
                            print("\nRemoval cancelled.")
                    else:
                        print("Invalid track number.")
                except ValueError:
                    print("Invalid input. Enter a number or N/P/Q.")
        return

    def deletePlaylist(self):
        """Delete an entire playlist"""
        self.updatePlaylistList()
        if not self.list:
            print("\nThere are no playlists to delete!")
            return
        
        print("\nSelect a playlist to delete:")
        self.displayPlaylists()
        
        try:
            idx = int(input("\nEnter playlist number: ")) - 1
            if idx < 0 or idx >= len(self.list):
                print("\nInvalid playlist number.")
                return
            
            playlist_name = self.list[idx]
            confirm = input(f"\nAre you sure you want to delete '{playlist_name}'? (y/n): ").lower()
            
            if confirm == 'y':
                for i, playlist in enumerate(self.data["Playlists"]):
                    if playlist_name in playlist:
                        self.data["Playlists"].pop(i)
                        save(self.data)
                        print(f"\nPlaylist '{playlist_name}' deleted successfully!")
                        self.updatePlaylistList()
                        return
            else:
                print("\nDeletion cancelled.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")