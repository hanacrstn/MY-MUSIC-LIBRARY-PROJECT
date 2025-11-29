
#TRACK CLASS

import json

class Track:
    def __init__(self, title, artist, album, additional_artists=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.additional_artists = additional_artists if additional_artists else []

    def add_additional_artist(self, artist_name):
        self.additional_artists.append(artist_name)

    def __str__(self):
        feat = ""
        if self.additional_artists:
            feat = " (ft. " + ", ".join(self.additional_artists) + ")"
        return f"Title: {self.title}{feat} | Artist: {self.artist} | Album: {self.album}"


class DurationTrack(Track):
    def __init__(self, title, artist, album, additional_artists=None, duration="00:00"):
        super().__init__(title, artist, album, additional_artists)
        self.duration_seconds = self._to_seconds(duration)

    def _to_seconds(self, duration):
        """Convert mm:ss string to total seconds."""
        minutes, seconds = map(int, duration.split(":"))
        return minutes * 60 + seconds

    def get_duration(self):
        """Return duration as mm:ss string."""
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def get_seconds(self):
        """Return duration in total seconds."""
        return self.duration_seconds

    def __str__(self):
        return f"{super().__str__()} | Duration: {self.get_duration()}"


class MusicLibrary:
    def __init__(self, filename="store.json"):
        self.filename = filename
        self.tracks = []

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.tracks = [self.load(d) for d in data.get("Tracks", []) if isinstance(d, dict)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tracks = []

    def load(self, d):
        if "title" in d and "artist" in d and "album" in d and "duration" in d:
            return DurationTrack(
                d["title"],
                d["artist"],
                d["album"],
                d.get("additional_artists", []),
                d["duration"]
            )
        return d

    def save(self):
        data = {"Tracks": []}
        i = 0
        while i < len(self.tracks):
            t = self.tracks[i]
            if isinstance(t, DurationTrack):
                data["Tracks"].append({
                    "title": t.title,
                    "artist": t.artist,
                    "album": t.album,
                    "additional_artists": t.additional_artists,
                    "duration": t.get_duration()
                })
            else:
                print("Skipping invalid track")
            i += 1

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_track(self):
        print('Enter "N" at any time to cancel.')

        title = input("Enter track title: ")
        if title.upper() == "N":
            print("Cancelled adding track.")
            return 

        artists = []
        while True:
            artist = input("Enter artist name: ")
            if artist.upper() == "N":
                print("Cancelled adding track.")
                return
            artists.append(artist)
            more = input("Add another artist? (Y/N): ")
            if more.upper() != "Y":
                break

        album = input("Enter the album: ")
        if album.upper() == "N":
            print("Cancelled adding track.")
            return
        
        while True:
            duration_input = input("Enter track duration (mm:ss): ")
            if duration_input.upper() == "N":
                print("Cancelled adding track.")
                return
            try:
                temp_track = DurationTrack("t", "t", "t", [], duration_input)
                duration_seconds = temp_track.get_seconds()
                break
            except (ValueError):
                print("Invalid format. Try mm:ss.")
    
