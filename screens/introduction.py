import pygame as pg
import sys

import Utils.constants as constants


background_introduction = pg.transform.scale(pg.image.load(constants.BACKGROUND_INTRO_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))


def introduction(screen, text_font, title_font):

    title_text = "¡¡ LA ULTIMA ESPERANZA !!"
    screen.blit(background_introduction, (0, 0))
    run = True

    # ----- lines height -----
    line_height = 40

    while run:
        # ----- read text -----
        with open('assets/intro_text.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        total_text_height = len(lines) * line_height
        start_y = screen.get_height() // 2 - total_text_height // 2

        # ----- intro logic -----
        for i, line in enumerate(lines):

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        run = False
                        return False # close intro screen, press F

                
            # ----- remove unnecessary spaces -----

            clean_line = line.strip() 


            # ----- render lines -----
            rendered_text = text_font.render(clean_line, True, constants.WHITE)
            rendered_title = title_font.render(title_text, True, constants.WHITE)

            # ----- title pos X and Y -----
            title_x = screen.get_width() // 2 - rendered_title.get_width() // 2
            title_y = 60 
            
            # ----- text pos X and Y -----
            x_pos = screen.get_width() // 2 - rendered_text.get_width() // 2
            y_pos = start_y + (i * line_height) # Posición Y se desplaza por cada línea
            
            # ----- draw texts -----
            screen.blit(rendered_title, (title_x, title_y))
            screen.blit(rendered_text, (x_pos, y_pos))
            
            # ----- draw skip text -----
            back_text = text_font.render("Presiona F para continuar", True, constants.GREEN)
            screen.blit(back_text, (constants.DISPLAY_WIDTH // 2 - back_text.get_width() // 2, constants.DISPLAY_HEIGTH - 100))
        
        pg.display.flip()

