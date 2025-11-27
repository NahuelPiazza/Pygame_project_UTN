import pygame as pg
import Utils.constants as constants

# pantalla de menu inicio

pg.font.init()

# < --------------------- variables y constantes --------------------- >

screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH))
background_menu = pg.transform.scale(pg.image.load(constants.BACKGROUND_MENU_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
button_font = pg.font.Font(constants.FONT_PATH, 35)
text_start_button = button_font.render("Start", True, (190,190,190))
text_exit_button = button_font.render("Exit", True, (190,190,190))
text_ranking_button = button_font.render("ranking", True, (190,190,190))
text_credits_button = button_font.render("credits", True, (190,190,190) )

volume_on = pg.image.load(constants.VOLUME_ON_BUTTON_PATH).convert_alpha()
volume_on = pg.transform.scale(volume_on, (80, 80))
volume_on.set_colorkey(constants.BLACK)

volume_off = pg.image.load(constants.VOLUME_OFF_BUTTON_PATH).convert_alpha()
volume_off = pg.transform.scale(volume_off, (80, 80))
volume_off.set_colorkey(constants.BLACK)

# < --------------------- funcion principal(dibujar menu) --------------------- >

def draw_menu(title_font, border_font, menu_button,start_button,credits_button, exit_button, ranking_button, volume_button, is_volume_on):
    
    screen.blit(background_menu, (0, 0))

    
    # renderiza y dibuja el título del juego
    title_text = title_font.render("Galaxnoid", True, constants.WHITE)
    title_rect = title_text.get_rect()

    # sombreado del título
    borde_surf = border_font.render("Galaxnoid", True, constants.BLACK)
    borde_rect =title_rect.move((screen.get_width() // 2 - title_text.get_width() // 2 + 10, screen.get_height() // 2 - 300))

    #pegamos titulo y sombreado
    screen.blit(borde_surf, borde_rect)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2 + 5, screen.get_height() // 2 - 300))

    #colocamos imagen de boton
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 - 150))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 - 30))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 + 90))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 150, screen.get_height() // 2 + 210))

    # dibuja el boton de volumen
    if is_volume_on:
        screen.blit(volume_on, (volume_button.x, volume_button.y))
    else:
        screen.blit(volume_off, (volume_button.x, volume_button.y))
    
    # dibuja el texto de los botones y los pega (REVISAR LOS VALORES --> ######## REDUCIR CODIGO ########)
    screen.blit(text_start_button, (start_button.x + (start_button.width - text_start_button.get_width()) // 2 - 20 , start_button.y + (start_button.height - text_start_button.get_height()) // 2 - 30 ))
    screen.blit(text_exit_button, (exit_button.x + (exit_button.width - text_exit_button.get_width()) // 2 - 20, exit_button.y + (exit_button.height - text_exit_button.get_height()) // 2 -10))
    screen.blit(text_ranking_button, (ranking_button.x + (ranking_button.width - text_ranking_button.get_width()) // 2 - 20 , ranking_button.y + (ranking_button.height - text_ranking_button.get_height()) // 2 - 35))
    screen.blit(text_credits_button, (credits_button.x + (credits_button.width - text_credits_button.get_width()) // 2 - 20 , credits_button.y + (credits_button.height - text_credits_button.get_height()) // 2 - 35))