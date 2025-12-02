from Track import Track
from Util_Jason import load, save  
from Duration import total_duration, sec_to_min
from Sorting import merge_sort  

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

    def createPlaylist(self):
        while True:
            playlistName = input("Enter Playlist Name: ")
            try:
                if "Playlists" not in self.data:
                    self.data["Playlists"] = []

                for playlist in self.data["Playlists"]:
                    if playlistName in playlist:
                        print("\nName already taken. Please choose another name.\n")
                        break

                else:  
                    self.data["Playlists"].append({playlistName: []})
                    save(self.data) 
                    print("\nPlaylist added successfully!\n")
                    
                    self.updatePlaylistList() 
                    break  

            except Exception as e:
                print(f"Error adding playlist: {e}")

    def displayTracks(self, playlist_index):
        self.updatePlaylistList()
        try:
            playlist_index = int(playlist_index) - 1

            playlist_name = self.list[playlist_index]

            for playlist in self.data["Playlists"]:
                if playlist_name in playlist:
                    tracks = playlist[playlist_name]
                    if not tracks:
                        print("\nNo tracks found in this playlist.")
                        return

                    print ("=" * 45)
                    print(f"Tracks in '{playlist_name}':")
                    print (f"Total duration: {total_duration(playlist, playlist_name)}")
                    sorted_tracks = merge_sort(tracks, key="title")
                    counter = 1
                    for track in sorted_tracks:
                        print(f"\t{counter}. {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
                        counter += 1
                    print ("=" * 45)
                    return

        except (ValueError, IndexError):
            print("\nInvalid input. Please enter a valid playlist number.")
    
    def displayPlaylists(self):
        self.updatePlaylistList()
        if not self.list:
            print("There are no Playlists made!")
            return
        
        counter = 1
        for playlist_name in self.list:
            print(f"    [{counter}] {playlist_name}")
            counter += 1


    def searchTrack(self, track):
        self.data = load()

        tracks = self.data.get("Tracks", [])
        if not tracks:
            print("\nNo tracks available in the music library.")
            return []

        track_lower = track.lower()
        results = [
            track for track in tracks
            if track_lower in track["title"].lower()
            or track_lower in track["artist"].lower()
            or track_lower in track["album"].lower()
        ]

        print(f"\nTracks matching '{track}':")
        
        counter = 1
        for track in results:
            print(f"    [{counter}] {track['title']} by {track['artist']} ({track['duration']})")
            counter += 1

        return results


    def searchedTracks(self, option, playlist_name, matching_tracks):
        for playlist in self.data["Playlists"]:
            if playlist_name in playlist:
                playlist_tracks = playlist[playlist_name]

                if option == 1:
                    try:
                        track_index = int(input("\nSelect a track to add (Enter number): ")) - 1
                        if track_index < 0 or track_index >= len(matching_tracks):
                            print("\nInvalid track selection.")
                            return

                        selected_track = matching_tracks[track_index]

                        if selected_track in playlist_tracks:
                            print("\nTrack is already in the playlist.")
                        else:
                            playlist_tracks.append(selected_track)
                            save(self.data)
                            print(f"\nTrack '{selected_track['title']}' added to playlist '{playlist_name}'.")
                    except ValueError:
                        print("\nInvalid input. Please enter a valid number.")

                elif option == 2:
                    added_count = 0
                    for selected_track in matching_tracks:
                        if selected_track not in playlist_tracks:
                            playlist_tracks.append(selected_track)
                            added_count += 1
                        else:
                            print(f"\nTrack '{selected_track['title']}' is already in the playlist.")

                    if added_count > 0:
                        save(self.data)
                        print(f"\n{added_count} tracks added to playlist '{playlist_name}'.")
                    else:
                        print("\nNo new tracks were added as all matching tracks are already in the playlist.")
                else:
                    print("\nInvalid option selected.")
                return


    def addTrack(self, playlist_name):
        for playlist in self.data["Playlists"]:
            if playlist_name in playlist:
                playlist_tracks = playlist[playlist_name]

                try:
                    index = int(input("\nSelect a track to add (Enter number): ")) - 1
                    if index < 0 or index >= len(self.data["Tracks"]):
                        print("\nInvalid track selection.")
                        return

                    selected_track = self.data["Tracks"][index]

                    if selected_track in playlist_tracks:
                        print("\nTrack is already in the playlist.")
                    else:
                        playlist_tracks.append(selected_track)
                        save(self.data)
                        print(f"\nTrack '{selected_track['title']}' added to playlist '{playlist_name}'.")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")
                return
