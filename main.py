import sys

import pygame as pg

from screens import main_menu, introduction, ranking_screen, game_over, in_game, credits
from Utils import functions,constants

pg.init()
pg.font.init()
pg.mixer.init()

# < --------------------- seteamos ancho y alto de pantalla --------------------- >

screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH))

# < --------------------- colocamos el icono y titulo de la ventana --------------------- >

pg.display.set_icon(pg.image.load(constants.ICON_PATH).convert())
pg.display.set_caption("Galaxnoid!")

# < --------------------- Definir fuentes para los elementos --------------------- >

gral_text_font = pg.font.Font(constants.FONT_PATH, 25)
intro_text_font = pg.font.Font(constants.FONT_PATH, 14)
title_font = pg.font.Font(constants.FONT_PATH, 74)
border_font = pg.font.Font(constants.FONT_PATH, 75)
game_over_font = pg.font.Font(constants.FONT_PATH, 20)


# < --------------------- contenedores Botones del menú ------------------- >

start_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 100 , constants.DISPLAY_HEIGTH // 2 - 110 , 250, 80)
ranking_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 15, 250, 80)
exit_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 102, constants.DISPLAY_HEIGTH // 2 + 230, 250, 80)
credits_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 135, 250, 80)
volume_button = pg.Rect(15, 690, 50, 50)

# < --------------------- cargar y escalar imagenes botones --------------------- >

menu_button = pg.image.load(constants.MENU_BUTTON_PATH).convert_alpha()
menu_button = pg.transform.scale(menu_button, (constants.DISPLAY_WIDTH // 2 - 150 , constants.DISPLAY_HEIGTH // 2 - 290))

# << ------------------------------------------------------------- bucle principal del juego ------------------------------------------------------------- >>

def main():

    # --------------------- variables del juego ---------------------

    clock = pg.time.Clock()
    run = True
    mostra_menu = True
    introducction = True
    game_music_playing = False
    intro_music_playing = False
    is_volume_on = True


    # --------------------- musica del menu ---------------------

    functions.activeate_music_menu()
    
    # --------------------- sonido botones ---------------------

    button_sound = pg.mixer.Sound(constants.BUTTON_SOUND_PATH)
    button_sound.set_volume(0.1)

    # --------------------- bucle principal del juego ---------------------

    while run:
        
        clock.tick(60)  # Limitar a 60 FPS
        

        # entrega la lista de eventos que pueden ocurrir en el juego
        for event in pg.event.get():
            # si el tipo de evento coincide con el evento de salir
            if event.type == pg.QUIT:
                run = False # Salir del juego  

        
            # -------------- funcionalidad botones del menu --------------
            elif event.type == pg.MOUSEBUTTONDOWN and mostra_menu:
                mouse_pos = pg.mouse.get_pos()

                if start_button.collidepoint(mouse_pos):
                    pg.mixer.music.stop()
                    button_sound.play()
                    mostra_menu = False # Iniciar el juego

                elif exit_button.collidepoint(mouse_pos):
                    button_sound.play()
                    run = False # Salir del juego 


                elif volume_button.collidepoint(mouse_pos):
                    is_volume_on = not is_volume_on
                    button_sound.play()
                    if is_volume_on:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()

                elif credits_button.collidepoint(mouse_pos):
                    credits.draw_credits(gral_text_font)
                    waiting_for_f = True

                    while waiting_for_f:

                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                run = False
                                waiting_for_f = False

                            elif event.type == pg.KEYDOWN:
                                if event.key == pg.K_f:
                                    waiting_for_f = False


                elif ranking_button.collidepoint(mouse_pos):
                    button_sound.play()
                    ranking_screen.draw_ranking(screen, title_font, gral_text_font)
                    pg.display.flip()
                    waiting_for_space = True

                    while waiting_for_space:

                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                run = False
                                waiting_for_space = False

                            elif event.type == pg.KEYDOWN:
                                if event.key == pg.K_SPACE:
                                    waiting_for_space = False
                    

            
        # --------------- lógica para mostrar pantallas --------------


        # ------ menú principal ------

        if mostra_menu:
            main_menu.draw_menu(title_font, border_font, menu_button, start_button, credits_button, exit_button, ranking_button, volume_button, is_volume_on )
        
        else:

        # ------ introducción al juego ------

            if introducction and not intro_music_playing:
                pg.mixer.music.load(constants.INTRO_MUSIC_PATH)
                pg.mixer.music.play(-1)     
                state = introduction.introduction(screen, intro_text_font, gral_text_font)
                introducction = state
                
            else:

        # ------ juego principal ------

                if not game_music_playing:
                    pg.mixer.music.load(constants.GAME_MUSIC_PATH)
                    pg.mixer.music.set_volume(0.2)
                    pg.mixer.music.play(-1)  
                    game_music_playing = True

                final_state = in_game.game(gral_text_font,intro_text_font)
                puntaje = final_state[2]

                if final_state[0] == True:  # game_over_screen
                    pg.mixer.music.stop()
                    game_over.game_over(screen,game_over_font, title_font, puntaje)
                    game_music_playing = False
                    mostra_menu = True
                    introducction = True
                    functions.activeate_music_menu()
                    

                elif final_state[1] == True:  # win_screen
                    pg.mixer.music.stop()
                    mostra_menu = True
                    introducction = True
                    game_music_playing = False
                    functions.activeate_music_menu()
                    

        # actualiza la pantalla
        pg.display.flip()


main()
pg.quit()
sys.exit()
    