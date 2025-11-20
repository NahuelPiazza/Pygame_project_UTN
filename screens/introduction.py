import pygame as pg
import sys

import constants

def introduction(screen, background_introduction, gral_text_font):
    screen.blit(background_introduction, (0, 0))
    intro_text = gral_text_font.render("introduccion al juego...", True, constants.BLACK)
    screen.blit(intro_text, (screen.get_width() // 2 - intro_text.get_width() // 2, screen.get_height() // 2 - intro_text.get_height() // 2))
    pg.display.flip()
    pg.time.delay(1000)  