import pygame as pg
import sys

import constants

def introduction(screen, background_introduction, text_font, title_font):

    title_text = "¡¡ ULTIMA ESPERANZA !!"

    screen.blit(background_introduction, (0, 0))

    # ----- espacio entre lineas -----
    line_height = 50

    # ----- leemos texto -----
    with open('intro_text.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    

    total_text_height = len(lines) * line_height
    start_y = screen.get_height() // 2 - total_text_height // 2

    # Iterar y dibujar cada línea
    for i, line in enumerate(lines):
        # Eliminar saltos de línea y espacios extra
        clean_line = line.strip() 
######################################################### REVISAR ESTA LOGICA | AGREGAR BOTON PARA SALTAR INTRO #########################################################
        # Renderizar la línea
        rendered_text = text_font.render(clean_line, True, constants.WHITE)
        rendered_title = title_font.render(title_text, True, constants.WHITE)

        # Calcular la posición del título (centrado horizontalmente)
        title_x = screen.get_width() // 2 - rendered_title.get_width() // 2
        
        # Colocarlo cerca de la parte superior (por ejemplo, a 50 píxeles del borde)
        title_y = 60 
        
        # Calcular posición 'X' (centrada) y 'Y' (usando el índice)
        x_pos = screen.get_width() // 2 - rendered_text.get_width() // 2
        y_pos = start_y + (i * line_height) # Posición Y se desplaza por cada línea
        
        # Dibujamos textos
        screen.blit(rendered_title, (title_x, title_y))
        screen.blit(rendered_text, (x_pos, y_pos))
    
    pg.display.flip()
    pg.time.delay(1000)  