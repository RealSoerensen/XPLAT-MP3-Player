from pydantic import FilePath
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pafy
from __init__ import ROOT
import os
import vlc


class Player():
    def __init__(self):
        self.instance = vlc.Instance()
        self.instance.log_unset()
        self.player = self.instance.media_player_new()

    def get_song(self, song):
        self.song = song
        if self.song.platform == "youtube":
            Player.YouTube(self.player, self.song, self.instance)
        elif self.song.platform == "spotify":
            pass
        elif self.song.platform == "soundcloud":
            Player.SoundCloud(self.player, self.song, self.instance)

    class YouTube():
        def __init__(self, player, song, instance):
            self.song = song
            self.instance = instance
            self.player = player

            self.play()

        def play(self):
            self.video = pafy.new(self.song.url)
            self.media = self.instance.media_new(self.video.getbest().url)
            self.player.set_media(self.media)
            self.player.play()

    class Spotify():
        def __init__(self, player, song, instance):
            self.song = song
            self.player = player
            self.instance = instance

            self.play()

        def play(self):
            pass

    class SoundCloud():
        def __init__(self, player, song, instance):
            self.song = song
            self.player = player
            self.instance = instance

            self.play()

        def play(self):
            self.media = self.instance.media_new(self.song.url)
            self.player.set_media(self.media)
            self.player.play()
