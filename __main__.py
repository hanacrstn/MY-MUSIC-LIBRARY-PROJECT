#MAIN Class

from Track import Track
from Library import MusicLibrary
from Playlist import Playlist
from Util_Jason import load, save
from Duration import total_duration
from Queues import Queue
from Sorting import merge_sort
from Pagination import Pagination

class main:
    def __init__(self):
        self.library = MusicLibrary()
        self.playlist = Playlist()
        self.data = load()
        self.queue = Queue()
        
        if self.queue.load_state():
            print("\n" + "=" * 60)
            print("Previous queue session restored!".center(60))
            print("=" * 60)

    @staticmethod
    def prompt(args: str) -> str:
        return input(args).lower()

    def banner(self, title):
        print("\n" + "╔" * 60)
        print(title.center(60))
        print("╔" * 60)

    def add_tracks_to_queue(self):
        """Add tracks to current queue from library or playlist"""
        while True:
            print("\n" + "=" * 60)
            print("ADD TRACKS TO QUEUE")
            print("=" * 60)
            print("1 → Add from Library")
            print("2 → Add from Playlist")
            print("0 → Back")
            
            choice = input("\nChoose: ").strip()
            
            if choice == '1':
                selected_track = self.library.displayTracksForSelection()
                if selected_track:
                    self.queue.enqueue(selected_track)
                    print(f"\n✓ Added '{selected_track['title']}' to queue!")
            
            elif choice == '2':
                selected_track = self._select_track_from_playlist()
                if selected_track:
                    self.queue.enqueue(selected_track)
                    print(f"\n✓ Added '{selected_track['title']}' to queue!")
            
            elif choice == '0':
                break

    def _select_track_from_playlist(self):
        """Helper to select a track from a playlist"""
        self.playlist.updatePlaylistList()
        
        print("\nSelect a playlist:")
        self.playlist.displayPlaylists()
        
        try:
            playlist_idx = int(input("\nEnter playlist number (0 to cancel): "))
            if playlist_idx == 0:
                return None
            
            if not 1 <= playlist_idx <= len(self.playlist.list):
                print("Invalid playlist number.")
                return None
            
            playlist_name = self.playlist.list[playlist_idx - 1]
            playlist_tracks = self.playlist._find_playlist_tracks(playlist_name)
            
            if not playlist_tracks:
                print("This playlist has no tracks.")
                return None
            
            sorted_tracks = merge_sort(playlist_tracks, key="title")
            return self._paginated_track_selection(sorted_tracks, f"Select Track from '{playlist_name}'")
            
        except ValueError:
            print("Invalid input.")
            return None

    def _paginated_track_selection(self, tracks, title):
        """Generic paginated track selection"""
        pagination = Pagination(tracks, items_per_page=10)
        
        while True:
            print("\n" + "=" * 60)
            print(f"{title} (Page {pagination.current_page}/{pagination.total_pages()})")
            print("=" * 60)
            
            page_tracks = pagination.get_page_items(pagination.current_page)
            start_index = pagination.start() + 1
            
            from Duration import sec_to_min
            for idx, track in enumerate(page_tracks, start=start_index):
                feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
                print(f"\t[{idx}] {track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})")
            
            print("\n" + "-" * 60)
            print("Enter track number | N → Next | P → Previous | Q → Cancel")
            print("-" * 60)
            
            track_choice = input("Choose: ").lower()
            
            if track_choice == 'n':
                if pagination.current_page < pagination.total_pages():
                    pagination.next_page()
                else:
                    print("Already at the last page.")
            elif track_choice == 'p':
                if pagination.current_page > 1:
                    pagination.previous_page()
                else:
                    print("Already at the first page.")
            elif track_choice == 'q':
                return None
            else:
                try:
                    selection = int(track_choice) - 1
                    if 0 <= selection < len(tracks):
                        return tracks[selection]
                    print("Invalid track number.")
                except ValueError:
                    print("Invalid input.")

    def show_current_queue(self):
        """Display the current queue"""
        if self.queue.size == 0:
            print("\nQueue is empty.")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.banner("CURRENT QUEUE")
            print(f"Total Tracks: {self.queue.size}")
            print(f"Now Playing: {self.queue.current_play()}")
            print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}")
            print("=" * 60)
            print(self.queue.display())
            print("\n" + "-" * 60)
            print("Q → Back")
            print("-" * 60)
            
            if input("\nChoose: ").lower() == 'q':
                break

    def _play_queue(self):
        """Generic queue player - handles all playback"""
        while True:
            if self.queue.size == 0:
                print("\nQueue is now empty. All tracks have been played.")
                break
            
            print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}\n")
            print(self.queue)
            print("\nOPTIONS:")
            print("  N → Next Track")
            print("  1 → Playback Settings (Shuffle / Repeat)")
            print("  2 → Exit Player")

            choice = main.prompt("Enter choice: ")

            if choice == '2':
                break
            elif choice == 'n':
                result = self.queue.next()
                if isinstance(result, dict):
                    print(f"NOW PLAYING: {self.queue.current_play()}")
                else:
                    print(result)
            elif choice == '1':
                self._playback_settings()

    def _playback_settings(self):
        """Handle playback settings menu"""
        print("\nPlayback Options:")
        print("  1 → Toggle Shuffle")
        print("  2 → Toggle Repeat")
        opt = main.prompt("Choose: ")
        if opt == '1':
            self.queue.toggle_shuffle()
            print(f"Shuffle: {self.queue.shuffle_status()}")
        elif opt == '2':
            self.queue.toggle_repeat()
            print(f"Repeat: {self.queue.repeat_status()}")

    def _music_player_menu(self):
        """Handle music player submenu"""
        while True:
            self.banner("MUSIC PLAYER")
            
            if self.queue.size > 0:
                print("R → Resume Previous Queue")
            
            print("1 → Play Music From Library (All Tracks)")
            print("2 → Play Music From Playlist")
            print("3 → Add Tracks to Queue")
            print("4 → Show Current Queue")
            print("5 → Clear Queue")
            print("0 → Return to Main Menu")

            choice = main.prompt("Enter choice: ")
            
            if choice == 'r' and self.queue.size > 0:
                print(f"\nResuming: {self.queue.current_play()}\n")
                self._play_queue()

            elif choice == '1':
                self._play_from_library()

            elif choice == '2':
                self._play_from_playlist()
            
            elif choice == '3':
                self.add_tracks_to_queue()
            
            elif choice == '4':
                self.show_current_queue()
            
            elif choice == '5':
                if input("Clear queue? All data will be lost. (y/n): ").lower() == 'y':
                    self.queue.clear_queue()
                    print("\nQueue cleared successfully!")
            
            elif choice == '0':
                break

    def _play_from_library(self):
        """Play all tracks from library"""
        try:
            self.data = load()
            tracks = merge_sort(self.data["Tracks"][:], "title")
            self.queue = Queue()

            self.banner("PLAYING FROM LIBRARY")
            print(f"Total Duration: {total_duration(self.data, 'Tracks')}\n")

            for t in tracks:
                self.queue.enqueue(t)

            print(f"NOW PLAYING: {self.queue.current_play()}\n")
            self._play_queue()

        except Exception as e:
            print(f"Error: {e}")
            if main.prompt("Try again? (y/n): ") == 'y':
                self._play_from_library()

    def _play_from_playlist(self):
        """Play tracks from selected playlist"""
        self.banner("PLAYING FROM PLAYLIST")
        print("Select a playlist:\n")

        self.playlist.displayPlaylists()
        print("0 → Go Back")

        try:
            playlist_choice = int(main.prompt("Enter number: "))
            self.playlist.updatePlaylistList()

            if playlist_choice == 0:
                return
            if not 1 <= playlist_choice <= len(self.playlist.list):
                print("Invalid playlist number.")
                return

            playlist_name = self.playlist.list[playlist_choice - 1]
            playlist_tracks = self.playlist._find_playlist_tracks(playlist_name)

            if not playlist_tracks:
                print("This playlist has no tracks.")
                return

            sorted_tracks = merge_sort(playlist_tracks, key="title")
            self.queue = Queue()
            self.queue.enqueue_playlist(sorted_tracks)

            print(f"NOW PLAYING FROM: {playlist_name}\n")
            print(f"NOW PLAYING: {self.queue.current_play()}\n")

            self._play_queue()

        except ValueError:
            print("Invalid input. Enter a valid number.")

    def _playlist_manager_menu(self):
        """Handle playlist manager submenu"""
        while True:
            self.playlist.data = load()  # Reload data at start of each loop
            self.playlist.updatePlaylistList()
            
            self.banner("PLAYLIST MANAGER")
            print("\nV → View All Playlists (Paginated)")
            print("A → Add Tracks to Playlist")
            print("R → Remove Track from Playlist")
            print("D → Delete Playlist")
            print("S → Select Playlist to View Tracks")
            print("E → Exit to Main Menu")

            choice = main.prompt("Choose: ")

            if choice == 'v':
                self.playlist.displayPlaylists(with_pagination=True)
            elif choice == 's':
                print("\nSelect a playlist:")
                self.playlist.displayPlaylists()
                try:
                    index = int(input("Enter number: "))
                    self.playlist.displayTracks(index)
                except:
                    print("Invalid selection.")
            elif choice == 'r':
                self._remove_track_from_playlist()
            elif choice == 'd':
                self.playlist.deletePlaylist()
            elif choice == 'a':
                self._add_track_to_playlist()
            elif choice == 'e':
                break
            else:
                try:
                    index = int(choice)
                    self.playlist.displayTracks(index)
                except:
                    print("Invalid selection.")

    def _remove_track_from_playlist(self):
        """Remove track from playlist helper"""
        self.playlist.data = load()  # Reload data
        self.playlist.updatePlaylistList()
        
        print("\nSelect a playlist:")
        self.playlist.displayPlaylists()
        try:
            idx = int(input("Enter number: ")) - 1
            if not 0 <= idx < len(self.playlist.list):
                print("Invalid playlist.")
                return
            playlist_name = self.playlist.list[idx]
            self.playlist.removeTrackFromPlaylist(playlist_name)
        except ValueError:
            print("Invalid input.")

    def _add_track_to_playlist(self):
        """Add track to playlist helper"""
        self.playlist.data = load()  # Reload data to get latest playlists
        self.playlist.updatePlaylistList()
        
        print("\nSelect a playlist:")
        self.playlist.displayPlaylists()
        try:
            idx = int(input("Enter number: ")) - 1
            if not 0 <= idx < len(self.playlist.list):
                print("Invalid playlist.")
                return
            playlist_name = self.playlist.list[idx]
        except ValueError:
            print("Invalid playlist.")
            return

        while True:
            print("\n1 → Add From All Tracks")
            print("2 → Search Tracks")
            print("0 → Cancel")
            
            choice_input = input("Choose: ").strip()
            
            if not choice_input:
                print("Invalid input. Please enter a valid choice.")
                continue
            
            try:
                opt = int(choice_input)
                if opt == 1:
                    self.playlist.addTrack(playlist_name)
                    break
                elif opt == 2:
                    if self._search_and_add_tracks(playlist_name):
                        break
                elif opt == 0:
                    print("Operation cancelled.")
                    break
                else:
                    print("Invalid option. Please choose 1, 2, or 0.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _search_and_add_tracks(self, playlist_name):
        """Search and add tracks to playlist"""
        query = input("Search: ").strip()
        if not query:
            print("Search query cannot be empty.")
            return False
        
        matches = self.playlist.searchTrack(query)
        if matches is None:
            return True
        if not matches:
            print("No matching tracks.")
            return False
        
        print("\n1 → Add One")
        print("2 → Add All")
        print("0 → Cancel")
        
        sub_input = input("Choose: ").strip()
        if not sub_input:
            print("Invalid input. Please enter a valid choice.")
            return False
        
        sub = int(sub_input)
        return self.playlist.searchedTracks(sub, playlist_name, matches) or sub == 0

    def main(self):
        """Main application loop"""
        while True:
            self.banner("GROUP 3'S MUSIC PLAYER")
            print("Press [M] to Open Music Player".center(60))
            print("╔" * 60)

            print("MAIN MENU")
            print("-" * 45)
            print("  1 → Create New Track")
            print("  2 → View All Tracks")
            print("  3 → Delete Track")
            print("  4 → Create Playlist")
            print("  5 → View All Playlists")
            print("  0 → Exit Program")
            print("-" * 45)

            choice = main.prompt("Enter choice: ")

            if choice == "m":
                self._music_player_menu()
            elif choice == '1':
                self.library.createTrack()
                self.data = load()
            elif choice == '2':
                self.banner("MUSIC LIBRARY")
                print(f"Total Duration: {self.library.getTotalDuration()}\n")
                self.library.displayTracks()
            elif choice == '3':
                self.banner("DELETE TRACK")
                self.library.deleteTrack()
                self.data = load()
            elif choice == '4':
                self.playlist.createPlaylist()
            elif choice == '5':
                self._playlist_manager_menu()
            elif choice == '0':
                print("Goodbye!")
                break

if __name__ == "__main__":
    run = main()
    run.main()
