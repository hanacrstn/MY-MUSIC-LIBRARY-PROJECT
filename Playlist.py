from Util_Jason import load, save
from Duration import sec_to_min, format_duration
from Sorting import merge_sort
from Pagination import Pagination

class Playlist:
    def __init__(self):
        self.data = load()
        self.list = []
        self.updatePlaylistList()  # Initialize list on creation

    def updatePlaylistList(self):
        """FIXED: Always reload data to ensure sync"""
        self.data = load()
        self.list = [name for playlist in self.data.get("Playlists", []) for name in playlist]

    def _track_exists_in_playlist(self, track, playlist_tracks):
        """Check if track already exists in playlist"""
        return any(t["id"] == track["id"] or 
                   (t["title"].lower() == track["title"].lower() and 
                    t["artist"].lower() == track["artist"].lower())
                   for t in playlist_tracks)

    def _find_playlist_tracks(self, playlist_name):
        """Find and return tracks for a specific playlist"""
        # Reload data to ensure freshness
        self.data = load()
        for playlist in self.data.get("Playlists", []):
            if playlist_name in playlist:
                return playlist[playlist_name]
        return None

    def _paginated_selection(self, items, title, item_formatter, allow_selection=False):
        """Generic paginated selection interface"""
        if not items:
            print(f"\nNo {title.lower()} found.")
            return None
        
        pagination = Pagination(items, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"{title} (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_items = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            for idx, item in enumerate(page_items, start=start_index):
                print(f"\t[{idx}] {item_formatter(item)}")
            
            print("\n" + "-" * 60)
            action_text = "Enter number | " if allow_selection else ""
            print(f"{action_text}N → Next | P → Previous | Q → {'Cancel' if allow_selection else 'Back'}")
            print("-" * 60)
            
            choice = input("Choose: ").lower().strip()
            
            if choice == 'n':
                pagination.next_page() if pagination.current_page < pagination.total_pages() else print("Already at the last page.")
            elif choice == 'p':
                pagination.previous_page() if pagination.current_page > 1 else print("Already at the first page.")
            elif choice == 'q':
                return None
            elif allow_selection and choice.isdigit():
                try:
                    selection = int(choice) - 1
                    if 0 <= selection < len(items):
                        return items[selection]
                    print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")

    def createPlaylist(self):
        """Create a new playlist with validation"""
        while True:
            playlistName = input("Enter Playlist Name: ").strip()
            
            if not playlistName:
                print("\nPlaylist name cannot be empty. Please try again.\n")
                continue
            
            # Reload to check for existing names
            self.data = load()
            
            if "Playlists" not in self.data:
                self.data["Playlists"] = []

            if any(existing_name.lower() == playlistName.lower() 
                   for playlist in self.data["Playlists"] 
                   for existing_name in playlist.keys()):
                print("\n" + "!" * 60)
                print("ERROR: Playlist name already exists!".center(60))
                print("!" * 60 + "\n")
                continue

            self.data["Playlists"].append({playlistName: []})
            save(self.data)
            print("\n" + "=" * 60)
            print("✓ Playlist added successfully!".center(60))
            print(f"'{playlistName}' created.".center(60))
            print("=" * 60 + "\n")
            self.updatePlaylistList()
            break

    def displayTracks(self, playlist_index):
        """Display tracks in a specific playlist with pagination"""
        self.updatePlaylistList()  # Ensure fresh data
        
        try:
            playlist_name = self.list[int(playlist_index) - 1]
            playlist_tracks = self._find_playlist_tracks(playlist_name)
            
            if playlist_tracks is None:
                print("\nPlaylist not found.")
                return
            
            if not playlist_tracks:
                print("\nNo tracks found in this playlist.")
                return

            sorted_tracks = merge_sort(playlist_tracks, key="title")
            total_secs = sum(int(t.get("duration", 0)) for t in playlist_tracks)
            
            def track_formatter(track):
                feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                return f"{track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})"
            
            pagination = Pagination(sorted_tracks, items_per_page=10)
            while True:
                print("\n" + "=" * 60)
                print(f"Playlist: '{playlist_name}' (Page {pagination.current_page}/{pagination.total_pages()})")
                print(f"Total duration: {format_duration(total_secs)}")
                print("=" * 60)
                
                for idx, track in enumerate(pagination.get_page_items(pagination.current_page), 
                                           start=pagination.start() + 1):
                    print(f"\t{idx}. {track_formatter(track)}")
                
                print("\n" + "-" * 60)
                print("N → Next Page | P → Previous Page | Q → Back")
                print("-" * 60)
                
                choice = input("Choose: ").lower()
                if choice == 'n':
                    pagination.next_page() if pagination.current_page < pagination.total_pages() else print("Already at the last page.")
                elif choice == 'p':
                    pagination.previous_page() if pagination.current_page > 1 else print("Already at the first page.")
                elif choice == 'q':
                    break
                else:
                    print("Invalid option.")
        except (ValueError, IndexError):
            print("\nInvalid input. Please enter a valid playlist number.")
    
    def displayPlaylists(self, with_pagination=False, allow_selection=False):
        """Display all playlists"""
        self.updatePlaylistList()  # Ensure fresh data
        
        if not self.list:
            print("There are no Playlists made!")
            return None
        
        if not with_pagination:
            for i, name in enumerate(self.list, 1):
                print(f"    [{i}] {name}")
            return None
        else:
            pagination = Pagination(self.list, items_per_page=10)
            while True:
                print("\n" + "=" * 60)
                print(f"Available Playlists (Page {pagination.current_page}/{pagination.total_pages()})")
                print("=" * 60)
                
                for idx, name in enumerate(pagination.get_page_items(pagination.current_page), 
                                          start=pagination.start() + 1):
                    print(f"    [{idx}] {name}")
                
                print("\n" + "-" * 60)
                print("N → Next Page | P → Previous Page | Q → Back")
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
                    return None
                else:
                    if choice:
                        print("Invalid option.")

    def searchTrack(self, track):
        """Search for tracks across library"""
        self.data = load()
        tracks = self.data.get("Tracks", [])
        if not tracks:
            print("\nNo tracks available in the music library.")
            return None

        track_lower = track.lower()
        results = [t for t in tracks if track_lower in t["title"].lower() or 
                   track_lower in t["artist"].lower() or track_lower in t["album"].lower()]

        if not results:
            return []

        def track_formatter(t):
            feat = f" (ft. {t.get('featured_artist', '')})" if t.get('featured_artist') else ""
            return f"{t['title']}{feat} by {t['artist']} ({t['duration']})"
        
        pagination = Pagination(results, items_per_page=10)
        while True:
            print("\n" + "=" * 60)
            print(f"Search Results (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            for idx, t in enumerate(pagination.get_page_items(pagination.current_page), 
                                   start=pagination.start() + 1):
                print(f"    [{idx}] {track_formatter(t)}")
            
            print("\n" + "-" * 60)
            print("N → Next Page | P → Previous Page | Q → Continue | C → Cancel")
            print("-" * 60)
            
            choice = input("Choose: ").lower().strip()
            if choice == 'n':
                pagination.next_page() if pagination.current_page < pagination.total_pages() else print("Already at the last page.")
            elif choice == 'p':
                pagination.previous_page() if pagination.current_page > 1 else print("Already at the first page.")
            elif choice == 'q':
                break
            elif choice == 'c':
                print("\nSearch cancelled.")
                return None
        return results

    def searchedTracks(self, option, playlist_name, matching_tracks):
        """Add searched tracks to playlist"""
        # FIXED: Reload data before accessing
        self.data = load()
        playlist_tracks = self._find_playlist_tracks(playlist_name)
        
        if playlist_tracks is None:
            print("\nPlaylist not found.")
            return False

        if option == 1:
            try:
                track_input = input("\nSelect a track to add (Enter number or 0 to cancel): ").strip()
                if not track_input or int(track_input) == 0:
                    print("\nOperation cancelled.")
                    return False
                
                track_index = int(track_input) - 1
                if not 0 <= track_index < len(matching_tracks):
                    print("\nInvalid track selection.")
                    return False

                selected_track = matching_tracks[track_index]
                if self._track_exists_in_playlist(selected_track, playlist_tracks):
                    print(f"\n{'!' * 60}\nERROR: Track already in playlist!\n{'!' * 60}\n")
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
            for track in matching_tracks:
                if not self._track_exists_in_playlist(track, playlist_tracks):
                    playlist_tracks.append(track)
                    added_count += 1
                else:
                    skipped_count += 1
            
            if added_count > 0:
                save(self.data)
                print(f"\n{'=' * 60}\n✓ {added_count} track(s) added to '{playlist_name}'")
                if skipped_count > 0:
                    print(f"{skipped_count} duplicate(s) skipped")
                print("=" * 60 + "\n")
            else:
                print(f"\n{'!' * 60}\nNo new tracks added\n{'!' * 60}\n")
            return True
        
        return False

    def displayTracksForSelection(self):
        """Display tracks for selection"""
        self.data = load()  # Ensure fresh data
        tracks = merge_sort(self.data.get("Tracks", []), key="title")
        def track_formatter(t):
            feat = f" (ft. {t.get('featured_artist', '')})" if t.get('featured_artist') else ""
            return f"{t['title']}{feat} by {t['artist']} ({sec_to_min(t['duration'])})"
        return self._paginated_selection(tracks, "Select a Track", track_formatter, allow_selection=True)

    def addTrack(self, playlist_name):
        """Add a single track to playlist"""
        selected_track = self.displayTracksForSelection()
        if not selected_track:
            print("\nTrack addition cancelled.")
            return

        # FIXED: Reload to get fresh playlist data
        self.data = load()
        
        playlist_tracks = self._find_playlist_tracks(playlist_name)
        if playlist_tracks is None:
            print("\nPlaylist not found.")
            return

        if self._track_exists_in_playlist(selected_track, playlist_tracks):
            print(f"\n{'!' * 60}\nERROR: Track already in playlist!\n{'!' * 60}\n")
        else:
            playlist_tracks.append(selected_track)
            save(self.data)
            print(f"\n{'=' * 60}\n✓ Track added successfully!\n{'=' * 60}\n")

    def removeTrackFromPlaylist(self, playlist_name):
        """Remove a track from playlist"""
        self.data = load()
        
        playlist_tracks = self._find_playlist_tracks(playlist_name)
        if playlist_tracks is None or not playlist_tracks:
            print("\nThis playlist has no tracks to remove.")
            return
        
        sorted_tracks = merge_sort(playlist_tracks, key="title")
        
        def track_formatter(t):
            feat = f" (ft. {t.get('featured_artist', '')})" if t.get('featured_artist') else ""
            return f"{t['title']}{feat} by {t['artist']} ({sec_to_min(t['duration'])})"
        
        selected = self._paginated_selection(sorted_tracks, f"Remove Track from '{playlist_name}'", 
                                            track_formatter, allow_selection=True)
        
        if selected:
            if input(f"\nRemove '{selected['title']}'? (y/n): ").lower() == 'y':
                playlist_tracks.remove(selected)
                save(self.data)
                print(f"\nTrack '{selected['title']}' removed from playlist '{playlist_name}'.")
            else:
                print("\nRemoval cancelled.")

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
            if not 0 <= idx < len(self.list):
                print("\nInvalid playlist number.")
                return
            
            playlist_name = self.list[idx]
            if input(f"\nAre you sure you want to delete '{playlist_name}'? (y/n): ").lower() == 'y':
                # Reload to ensure we're modifying fresh data
                self.data = load()
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
