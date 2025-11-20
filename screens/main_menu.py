import pygame as pg
import constants
# pantalla de menu inicio
def draw_menu(screen,background_menu, title_font, border_font, menu_button, text_start_button, text_exit_button, text_ranking_button,start_button, exit_button, ranking_button):
    screen.blit(background_menu, (0, 0))

    
    # renderiza y dibuja el título del juego
    title_text = title_font.render("Galaxnoid", True, constants.WHITE)
    title_rect = title_text.get_rect()
    # sombreado del título
    borde_surf = border_font.render("Galaxnoid", True, constants.BLACK)
    borde_rect =title_rect.move((screen.get_width() // 2 - title_text.get_width() // 2 + 10, screen.get_height() // 2 - 200))

    #pegamos titulo y sombreado
    screen.blit(borde_surf, borde_rect)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2 + 5, screen.get_height() // 2 - 200))

    #colocamos imagen de boton
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 - 20))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 + 110))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 + 240))
    
    # dibuja el texto de los botones y los pega
    screen.blit(text_start_button, (start_button.x + (start_button.width - text_start_button.get_width()) // 2 - 18, start_button.y + (start_button.height - text_start_button.get_height()) // 2 ))
    screen.blit(text_exit_button, (exit_button.x + (exit_button.width - text_exit_button.get_width()) // 2 - 20, exit_button.y + (exit_button.height - text_exit_button.get_height()) // 2 + 155))
    screen.blit(text_ranking_button, (ranking_button.x + (ranking_button.width - text_ranking_button.get_width()) // 2 - 20, ranking_button.y + (ranking_button.height - text_ranking_button.get_height()) // 2 + 25))
