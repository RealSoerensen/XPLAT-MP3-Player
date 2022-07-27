import os
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pafy
from __init__ import ROOT
os.add_dll_directory(ROOT + r"\assets\dll")


class Player():
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
            pass



