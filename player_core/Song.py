class Song():
    def __init__(self,
                 album='',
                 albumartist='',
                 artist='',
                 disc=0,
                 title='',
                 track=0,
                 duration='',
                 file_path=''):
        
        self.album = album
        self.albumartist = albumartist
        self.artist = artist
        self.disc = disc
        self.title = title
        self.track = track
        self.duration = duration  # in milliseconds
        self.file_path = file_path

    def get_album(self):
        return self.album

    def get_albumartist(self):
        return self.albumartist
    
    def get_artist(self):
        return self.artist
    
    def get_disc(self):
        return self.disc
    
    def get_title(self):
        return self.title
    
    def get_track(self):
        return self.track
    
    def get_duration(self):
        return self.duration
    
    def get_file_path(self):
        return self.file_path
