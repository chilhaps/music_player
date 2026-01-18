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
