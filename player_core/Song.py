class Song():
    def __init__(self, title, artist, album, duration, file_path):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # in milliseconds
        self.file_path = file_path

    def get_title(self):
        return self.title
    
    def get_artist(self):
        return self.artist
    
    def get_album(self):
        return self.album
    
    def get_duration(self):
        return self.duration
    
    def get_file_path(self):
        return self.file_path
    
    def get_is_playable(self):
        # Here we can add logic to determine if the song is playable
        # For simplicity, we'll assume all songs are playable
        return True
    
    def get_format(self):
        # Extract file format from the file path
        return self.file_path.split('.')[-1]
