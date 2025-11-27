import pygame as pg
import sys

from Utils import constants


# < ------------------------ variables y constantes ------------------------ >

screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH))
background_game = pg.transform.scale(pg.image.load(constants.BACKGROUND_GAME_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
spaceship_sprite = pg.transform.scale(pg.image.load(constants.PLAYER_SPRITE_PATH).convert_alpha(), (150, 50))
ball_sprite = pg.transform.scale(pg.image.load(constants.BALL_SPRITE_PATH).convert_alpha(), (20, 20))
normal_brick = pg.transform.scale(pg.image.load(constants.NORMAL_BRICK_PATH).convert_alpha(), (70, 30))
special_brick = pg.transform.scale(pg.image.load(constants.SPECIAL_BRICK_PATH).convert_alpha(), (70, 30))

def game(gral_text_font,intro_text_font ):
    contador_vidas = 1
    puntaje = 0
    game_over_screen = False
    win_screen = False
    game_running = True
    paused = False

    # ----- configurar ladrillos ----
    #  --------------------- ladrillos ---------------------

    brick_width, block_height = normal_brick.get_size()
    brick_space = 5
    brick_rows = 6
    brick_columns = 13

    ladrillos = []
    inicio_x = (constants.DISPLAY_WIDTH // 2) - (brick_columns * (brick_width + brick_space)) // 2
    for fila in range(brick_rows):
        for col in range(brick_columns):
            ladrillo_x = inicio_x + col * (brick_width + brick_space)
            ladrillo_y = 50 + fila * (block_height + brick_space)
            ladrillos.append(normal_brick.get_rect(topleft=(ladrillo_x, ladrillo_y)))

    ladrillos.clear()

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
            
        # < -------------------  Condiciones de Fin de Juego  ------------------- > 
        
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
           

        # < ---------------- Dibujos (Renderizado) ------------------------- >

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
