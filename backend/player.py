import vlc


class Player():
    def __init__(self):
        self.instance = vlc.Instance()
        self.instance.log_unset()
        self.player = self.instance.media_player_new()

    def play_song(self, song):
        self.media = self.instance.media_new(song.url)
        self.player.set_media(self.media)
        self.player.play()
