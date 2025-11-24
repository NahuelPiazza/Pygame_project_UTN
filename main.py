import pygame as pg
import sys

import random

from ranking import add_score, get_ranking
from screens import main_menu, introduction, ranking_screen,game_over
from Utils import functions,constants

pg.init()
pg.mixer.init()

#--------------------- seteamos ancho y alto de pantalla ---------------------

screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH))

# --------------------- colocamos el icono y titulo de la ventana ---------------------

pg.display.set_icon(pg.image.load(constants.ICON_PATH).convert())
pg.display.set_caption("Galaxnoid!")

# --------------------- Definir fuentes para los elementos ---------------------

gral_text_font = pg.font.Font(constants.FONT_PATH, 25)
intro_text_font = pg.font.Font(constants.FONT_PATH, 15)
title_font = pg.font.Font(constants.FONT_PATH, 74)
border_font = pg.font.Font(constants.FONT_PATH, 75)
button_font = pg.font.Font(constants.FONT_PATH, 35)

# --------------------- cargar y escalar la imagenes ---------------------

background_menu = pg.transform.scale(pg.image.load(constants.BACKGROUND_MENU_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
background_introduction = pg.transform.scale(pg.image.load(constants.BACKGROUND_INTRO_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
background_game = pg.transform.scale(pg.image.load(constants.BACKGROUND_GAME_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
spaceship_sprite = pg.transform.scale(pg.image.load(constants.PLAYER_SPRITE_PATH).convert_alpha(), (150, 50))
ball_sprite = pg.transform.scale(pg.image.load(constants.BALL_SPRITE_PATH).convert_alpha(), (20, 20))
normal_brick = pg.transform.scale(pg.image.load(constants.NORMAL_BRICK_PATH).convert_alpha(), (70, 30))
special_brick = pg.transform.scale(pg.image.load(constants.SPECIAL_BRICK_PATH).convert_alpha(), (70, 30))

# --------------------- contenedores Botones del menú -------------------

start_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 10 , 250, 80)
ranking_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 140, 250, 80)
exit_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 250, 250, 80)
volume_button = pg.Rect(20, 710, 50, 50)

# --------------------- cargar y escalar imagenes botones --------------------- 

menu_button = pg.image.load(constants.MENU_BUTTON_PATH).convert_alpha()
menu_button = pg.transform.scale(menu_button, (constants.DISPLAY_WIDTH // 3 - 180, constants.DISPLAY_HEIGTH // 2 - 290))

volume_on = pg.image.load(constants.VOLUME_ON_BUTTON_PATH).convert_alpha()
volume_on = pg.transform.scale(volume_on, (80, 80))
volume_on.set_colorkey(constants.BLACK)

volume_off = pg.image.load(constants.VOLUME_OFF_BUTTON_PATH).convert_alpha()
volume_off = pg.transform.scale(volume_off, (80, 80))
volume_off.set_colorkey(constants.BLACK)

# --------------------- Textos de los botones ---------------------

text_start_button = button_font.render("Start", True, (190,190,190))
text_exit_button = button_font.render("Exit", True, (190,190,190))
text_ranking_button = button_font.render("ranking", True, (190,190,190))



#  ------------------------------------------------- pantalla del juego -----------------------------------------------------------------
def game():
    contador_vidas = 1
    puntaje = 0
    game_over_screen = False
    win_screen = False
    game_running = True
    paused = False

############################################################ LOGICA DE PELOTA, LADRILLOS Y NAVE --> HACERLA POR FUERA ############################################################

    global ladrillos # Acceso a variables globales

    # ----- configurar ladrillos -----
    #  --------------------- ladrillos ---------------------

    brick_width, block_height = normal_brick.get_size()
    brick_space = 5
    brick_rows = 5
    brick_columns = 18

    ladrillos = []
    inicio_x = (constants.DISPLAY_WIDTH // 2) - (brick_columns * (brick_width + brick_space)) // 2
    for fila in range(brick_rows):
        for col in range(brick_columns):
            ladrillo_x = inicio_x + col * (brick_width + brick_space)
            ladrillo_y = 50 + fila * (block_height + brick_space)
            ladrillos.append(normal_brick.get_rect(topleft=(ladrillo_x, ladrillo_y)))


    # ----------- posicionar pelota y nave al iniciar el juego -------------------

    # pelota
    PELOTA_RADIO = 10
    pelota_x = constants.DISPLAY_WIDTH // 2
    pelota_y = constants.DISPLAY_HEIGTH // 2
    pelota_rect = pg.Rect(pelota_x - PELOTA_RADIO, pelota_y - PELOTA_RADIO, 
                              PELOTA_RADIO * 2, PELOTA_RADIO * 2)
    pelota_rect.x = constants.DISPLAY_WIDTH // 2 - PELOTA_RADIO
    pelota_rect.y = constants.DISPLAY_HEIGTH // 2 - PELOTA_RADIO
    pelota_dx = 4
    pelota_dy = -4

    # nave
    character_sprite_rect = spaceship_sprite.get_rect(center=(constants.DISPLAY_WIDTH // 2,constants.DISPLAY_HEIGTH // 2 + 320))
    


    # reconstruir ladrillos si es necesario
    
    if len(ladrillos) == 0:
        inicio_x = (constants.DISPLAY_WIDTH // 2) - (brick_columns * (brick_width + brick_space)) // 2
        for fila in range(brick_rows):
            for col in range(brick_columns):
                ladrillo_x = inicio_x + col * (brick_width + brick_space)
                ladrillo_y = 50 + fila * (block_height + brick_space)
                ladrillos.append(normal_brick.get_rect(topleft=(ladrillo_x, ladrillo_y)))

    
    while game_running:

        # limitar a 60 fps
        pg.time.Clock().tick(60)
        
        # Limitar la nave a los bordes de la pantalla
        character_sprite_rect.x = max(0, character_sprite_rect.x)
        character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)


        # 1.  -------------- Movimiento de la Pelota ----------------
        if not paused:
            pelota_rect.x += pelota_dx
            pelota_rect.y += pelota_dy

            # 2. Manejo de Eventos
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
                
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    paused = not paused  # Alternar entre pausado y no pausado

        keys = pg.key.get_pressed()

        if not paused:

            if keys[pg.K_LEFT]:
                character_sprite_rect.x = max(0, character_sprite_rect.x)
                character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)
                character_sprite_rect.x -= 7
            if keys[pg.K_RIGHT]:
                character_sprite_rect.x = max(0, character_sprite_rect.x)
                character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)
                character_sprite_rect.x += 7
        if not paused:
        # 3. -------------- Lógica de Colisiones ----------------
            # -------- Colisión Izquierda
            if pelota_rect.left <= 0:
                pelota_dx = abs(pelota_dx) # Fuerza el rebote hacia la derecha
                pelota_rect.left = 0       # Corrige la posición
            # ------------ Colisión Derecha
            elif pelota_rect.right >= constants.DISPLAY_WIDTH:
                pelota_dx = -abs(pelota_dx) # Fuerza el rebote hacia la izquierda
                pelota_rect.right = constants.DISPLAY_WIDTH # Corrige la posición
            # ------------------ Colisión Superior
            if pelota_rect.top <= 0:
                pelota_dy = abs(pelota_dy) # Fuerza el rebote hacia abajo
                pelota_rect.top = 0      # Corrige la posición

            # --------- Colisión Pelota con la Nave (Pala)

            if pelota_rect.colliderect(character_sprite_rect) and pelota_dy > 0:
                # Solo rebota si la pelota baja
                pelota_dy *= -1 
                pelota_rect.bottom = character_sprite_rect.top # Asegura que no se atasque
                
                # Lógica de rebote angular (convertido a entero para Pygame)
                diferencia = pelota_rect.centerx - character_sprite_rect.centerx
                pelota_dx = int(diferencia * 0.15) 
                
                # Aseguramos una velocidad mínima en X para que no se mueva verticalmente (evita estancamiento)
                if abs(pelota_dx) < 1:
                    pelota_dx = 1 if diferencia > 0 else -1


        # C. Colisión Pelota con Ladrillos

        ladrillos_a_eliminar = []
        for ladrillo in ladrillos:
            if pelota_rect.colliderect(ladrillo):
                # Invertimos la dirección vertical y eliminamos el ladrillo
                pelota_dy *= -1
                
                # Ajustamos posición para evitar doble rebote
                pelota_rect.top = ladrillo.bottom if pelota_dy > 0 else ladrillo.top - pelota_rect.height

                ladrillos_a_eliminar.append(ladrillo)
                break # Solo un ladrillo a la vez

        # Eliminar los ladrillos golpeados
        for ladrillo in ladrillos_a_eliminar:
            ladrillos.remove(ladrillo)
            puntaje += 10
            
        # ------------- 4. Condiciones de Fin de Juego -------------------
        
        # Si la pelota cae por debajo de la nave 3 veces (Game Over)
        if pelota_rect.bottom >= constants.DISPLAY_HEIGTH:
            contador_vidas -= 1

            if contador_vidas <= 0:
                game_over_screen = True
                win_screen = False
                game_running = False
                return (game_over_screen, win_screen, puntaje)
            

            # vuelve a la posicion inicial
            pelota_rect.x = constants.DISPLAY_WIDTH // 2 - PELOTA_RADIO
            pelota_rect.y = constants.DISPLAY_HEIGTH // 2 - PELOTA_RADIO
            pelota_dx = 5
            pelota_dy = -5
            character_sprite_rect.center = (constants.DISPLAY_WIDTH // 2,constants.DISPLAY_HEIGTH // 2 + 320)

        
        if not ladrillos:
            print("¡VICTORIA!")
            win_screen = True
            game_over_screen = False
            game_running = False
            return (game_over_screen, win_screen, puntaje)
           
        




        # 5. ---------------- Dibujo (Renderizado) -------------------------

        screen.blit(background_game, (0, 0))

        # Dibujar Ladrillos
        for ladrillo in ladrillos:
            screen.blit(normal_brick, ladrillo)
            

        # Dibujar Nave (Pala)
        screen.blit(spaceship_sprite, character_sprite_rect)


        # Dibujar Pelota (usamos el centro del Rect para el círculo)
        screen.blit(ball_sprite, (pelota_rect.x, pelota_rect.y))

       



        # Dibujar vidas y puntaje
        vidas_text = gral_text_font.render(f"Vidas: {contador_vidas}", True, constants.WHITE)
        pause_button_text = intro_text_font.render("Pausa -> P ", True, constants.WHITE)
        puntaje_text = gral_text_font.render(f"Puntaje: {puntaje}", True, constants.WHITE)
        screen.blit(pause_button_text, (constants.DISPLAY_WIDTH // 2 - pause_button_text.get_width() // 2, 10))
        screen.blit(vidas_text, (10, 10))   
        screen.blit(puntaje_text, (constants.DISPLAY_WIDTH - puntaje_text.get_width() - 10, 10))

        if paused:
            pause_text = gral_text_font.render("PAUSADO - Presiona P para continuar", True, constants.WHITE)
            pause_rect = pause_text.get_rect(center=(constants.DISPLAY_WIDTH // 2, constants.DISPLAY_HEIGTH // 2))
            screen.blit(pause_text, pause_rect)

        pg.display.flip()


# ------------------------------------------------------------- bucle inicial del juego -------------------------------------------------------------
def main():

    # --------------------- variables del juego ---------------------

    clock = pg.time.Clock()
    run = True
    mostra_menu = True
    introducction = True
    game_music_playing = False
    intro_music_playing = False
    show_ranking = False
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
            main_menu.draw_menu(screen,background_menu, title_font, border_font, menu_button, text_start_button, text_exit_button, text_ranking_button,start_button, exit_button, ranking_button, volume_on, volume_off, volume_button, is_volume_on)
        
        else:

        # ------ introducción al juego ------

            if introducction and not intro_music_playing:
                pg.mixer.music.load(constants.INTRO_MUSIC_PATH)
                pg.mixer.music.play(-1)     
                introduction.introduction(screen, background_introduction, intro_text_font, gral_text_font)
                introducction = False
                
            else:

        # ------ juego principal ------

                if not game_music_playing:
                    pg.mixer.music.load(constants.GAME_MUSIC_PATH)
                    pg.mixer.music.play(-1)  
                    game_music_playing = True

                final_state = game()
                puntaje = final_state[2]

                print(final_state)
                if final_state[0] == True:  # game_over_screen
                    pg.mixer.music.stop()
                    game_over.game_over(screen, gral_text_font, title_font, puntaje)
                    game_music_playing = False
                    mostra_menu = True
                    introducction = True
                    ladrillos.clear()
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
    