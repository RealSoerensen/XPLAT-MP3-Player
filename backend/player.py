import pafy
import vlc


class Player():
    def __init__(self):
        self.instance = vlc.Instance()
        self.instance.log_unset()
        self.player = self.instance.media_player_new()

    def get_song(self, song):
        Player.LocalPlayer(self.player, song, self.instance)

    class LocalPlayer():
        def __init__(self, player, song, instance):
            self.song = song
            self.player = player
            self.instance = instance

            self.play()

        def play(self):
            self.media = self.instance.media_new(self.song.url)
            self.player.set_media(self.media)
            self.player.play()
