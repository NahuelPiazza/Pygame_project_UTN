import sys

import pygame as pg

from Utils import constants

def draw_credits(text_font):

    screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH))
    background = pg.transform.scale(pg.image.load(constants.BACKGROUND_GAME_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
    screen.blit(background, (0, 0))
     

    line_height = 50

    with open('assets/credits.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    total_text_height = len(lines) * line_height
    start_y = screen.get_height() // 2 - total_text_height // 2

    for i, line in enumerate(lines):
        # Eliminar saltos de línea y espacios extra
        clean_line = line.strip() 

        rendered_text = text_font.render(clean_line, True, constants.WHITE)
        x_pos = screen.get_width() // 2 - rendered_text.get_width() // 2
        y_pos = start_y + (i * line_height) # Posición Y se desplaza por cada línea
        screen.blit(rendered_text, (x_pos, y_pos))
        back_text = text_font.render("Presiona F para volver", True, constants.WHITE)
        screen.blit(back_text, (constants.DISPLAY_WIDTH // 2 - back_text.get_width() // 2, constants.DISPLAY_HEIGTH - 100))
    

    for event in pg.event.get():
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()

    pg.display.flip()
        
                
