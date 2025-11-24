import pygame as pg

def activeate_music_menu():
    pg.mixer.music.load('assets/music/music_menu.mp3')
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1)