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
        print("\n" + "═" * 60)
        print(title.center(60))
        print("═" * 60)

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
                print("\nSelect a playlist:")
                self.playlist.displayPlaylists()
                
                try:
                    playlist_idx = int(input("\nEnter playlist number (0 to cancel): "))
                    if playlist_idx == 0:
                        continue
                    
                    self.playlist.updatePlaylistList()
                    if playlist_idx < 1 or playlist_idx > len(self.playlist.list):
                        print("Invalid playlist number.")
                        continue
                    
                    playlist_name = self.playlist.list[playlist_idx - 1]
                    playlist_tracks = self.playlist._find_playlist_tracks(playlist_name)
                    
                    if not playlist_tracks:
                        print("This playlist has no tracks.")
                        continue
                    
                    sorted_tracks = merge_sort(playlist_tracks, key="title")
                    pagination = Pagination(sorted_tracks, items_per_page=10)
                    
                    while True:
                        print("\n" + "=" * 60)
                        print(f"Select Track from '{playlist_name}' (Page {pagination.current_page}/{pagination.total_pages()})")
                        print("=" * 60)
                        
                        page_tracks = pagination.get_page_items(pagination.current_page)
                        start_index = pagination.start() + 1
                        
                        for idx, track in enumerate(page_tracks, start=start_index):
                            from Duration import sec_to_min
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
                            break
                        else:
                            try:
                                selection = int(track_choice) - 1
                                if 0 <= selection < len(sorted_tracks):
                                    selected_track = sorted_tracks[selection]
                                    self.queue.enqueue(selected_track)
                                    print(f"\n✓ Added '{selected_track['title']}' to queue!")
                                    break
                                else:
                                    print("Invalid track number.")
                            except ValueError:
                                print("Invalid input.")
                    
                except ValueError:
                    print("Invalid input.")
            
            elif choice == '0':
                break

    def show_current_queue(self):
        """Display the current queue with pagination"""
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
            
            choice = input("\nChoose: ").lower()
            
            if choice == 'q':
                break

    def main(self):
        while True:
            self.banner("GROUP 3'S MUSIC PLAYER")
            print("Press [M] to Open Music Player".center(60))
            print("═" * 60)

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

                    elif choice == '1':
                        try:
                            self.data = load()
                            tracks = merge_sort(self.data["Tracks"][:], "title")
                            self.queue = Queue()

                            self.banner("PLAYING FROM LIBRARY")
                            print(f"Total Duration: {total_duration(self.data, 'Tracks')}\n")

                            for t in tracks:
                                self.queue.enqueue(t)

                            current = self.queue.current_play()
                            print(f"NOW PLAYING: {current}\n")

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

                        except Exception as e:
                            print(f"Error: {e}")
                            if main.prompt("Try again? (y/n): ") != 'y': 
                                break

                    elif choice == '2':
                        self.banner("PLAYING FROM PLAYLIST")
                        print("Select a playlist:\n")

                        self.playlist.displayPlaylists()
                        print("0 → Go Back")

                        try:
                            playlist_choice = int(main.prompt("Enter number: "))
                            self.playlist.updatePlaylistList()

                            if playlist_choice == 0:
                                continue
                            if playlist_choice < 0 or playlist_choice > len(self.playlist.list):
                                print("Invalid playlist number.")
                                continue

                            playlist_name = self.playlist.list[playlist_choice - 1]
                            playlist_tracks = []

                            for playlist in self.playlist.data["Playlists"]:
                                if playlist_name in playlist:
                                    playlist_tracks = playlist[playlist_name]
                                    break

                            if not playlist_tracks:
                                print("This playlist has no tracks.")
                                continue

                            sorted_tracks = merge_sort(playlist_tracks, key="title")
                            self.queue = Queue()
                            self.queue.enqueue_playlist(sorted_tracks)

                            print(f"NOW PLAYING FROM: {playlist_name}\n")
                            print(f"NOW PLAYING: {self.queue.current_play()}\n")

                            while True:
                                if self.queue.size == 0:
                                    print("\nQueue is now empty. All tracks have been played.")
                                    break
                                
                                print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}\n")
                                print(self.queue.display())

                                print("\nOPTIONS:")
                                print("  N → Next Track (Current will be removed)")
                                print("  1 → Playback Options")
                                print("  2 → Exit Player")

                                choice = main.prompt("Choose: ")

                                if choice == 'n':
                                    result = self.queue.next()
                                    if isinstance(result, dict):
                                        print(f"NOW PLAYING: {self.queue.current_play()}")
                                    else:
                                        print(result)
                                elif choice == '1':
                                    print("1 → Toggle Shuffle\n2 → Toggle Repeat")
                                    opt = main.prompt("Choose: ")
                                    if opt == '1': 
                                        self.queue.toggle_shuffle()
                                        print(f"Shuffle: {self.queue.shuffle_status()}")
                                    elif opt == '2': 
                                        self.queue.toggle_repeat()
                                        print(f"Repeat: {self.queue.repeat_status()}")
                                elif choice == '2': 
                                    break

                        except ValueError:
                            print("Invalid input. Enter a valid number.")
                    
                    elif choice == '3':
                        self.add_tracks_to_queue()
                    
                    elif choice == '4':
                        self.show_current_queue()
                    
                    elif choice == '5':
                        confirm = input("Clear queue? All data will be lost. (y/n): ").lower()
                        if confirm == 'y':
                            self.queue.clear_queue()
                            print("\nQueue cleared successfully!")
                    
                    elif choice == '0': 
                        break

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
                while True:
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
                        print("\nSelect a playlist:")
                        self.playlist.displayPlaylists()
                        try:
                            idx = int(input("Enter number: ")) - 1
                            if idx < 0 or idx >= len(self.playlist.list):
                                print("Invalid playlist.")
                                continue
                            playlist_name = self.playlist.list[idx]
                            self.playlist.removeTrackFromPlaylist(playlist_name)
                        except ValueError:
                            print("Invalid input.")
                    
                    elif choice == 'd':
                        self.playlist.deletePlaylist()
                    
                    elif choice == 'a':
                        print("\nSelect a playlist:")
                        self.playlist.displayPlaylists()
                        try:
                            idx = int(input("Enter number: ")) - 1
                            if idx < 0 or idx >= len(self.playlist.list): 
                                raise ValueError
                            playlist_name = self.playlist.list[idx]
                        except ValueError:
                            print("Invalid playlist.")
                            continue

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
                                    query = input("Search: ").strip()
                                    if not query:
                                        print("Search query cannot be empty.")
                                        continue
                                    matches = self.playlist.searchTrack(query)
                                    if matches is None:
                                        break
                                    if not matches:
                                        print("No matching tracks.")
                                        continue
                                    
                                    print("\n1 → Add One")
                                    print("2 → Add All")
                                    print("0 → Cancel")
                                    
                                    sub_input = input("Choose: ").strip()
                                    if not sub_input:
                                        print("Invalid input. Please enter a valid choice.")
                                        continue
                                    
                                    sub = int(sub_input)
                                    result = self.playlist.searchedTracks(sub, playlist_name, matches)
                                    if result or sub == 0:
                                        break
                                elif opt == 0:
                                    print("Operation cancelled.")
                                    break
                                else:
                                    print("Invalid option. Please choose 1, 2, or 0.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")

                    elif choice == 'e': 
                        break
                    else:
                        try:
                            index = int(choice)
                            self.playlist.displayTracks(index)
                        except:
                            print("Invalid selection.")

            elif choice == '0':
                print("Goodbye!")
                break

if __name__ == "__main__":
    run = main()
    run.main()
