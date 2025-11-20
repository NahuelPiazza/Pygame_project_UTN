import pygame as pg
import sys

from screens import main_menu, introduction
import constants

pg.init()
pg.mixer.init()

#--------------------- seteamos ancho y alto de pantalla ---------------------

screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH), pg.RESIZABLE)

# --------------------- colocamos el icono y titulo de la ventana ---------------------

pg.display.set_icon(pg.image.load(constants.ICON_PATH).convert())
pg.display.set_caption("Galaxnoid!")

# --------------------- Definir fuentes para los elementos ---------------------

gral_text_font = pg.font.Font(constants.FONT_PATH, 25)
title_font = pg.font.Font(constants.FONT_PATH, 74)
border_font = pg.font.Font(constants.FONT_PATH, 75)
button_font = pg.font.Font(constants.FONT_PATH, 35)

# --------------------- cargar y escalar la imagenes ---------------------

background_menu = pg.transform.scale(pg.image.load(constants.BACKGROUND_MENU_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
background_introduction = pg.transform.scale(pg.image.load(constants.BACKGROUND_INTRO_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
background_game = pg.transform.scale(pg.image.load(constants.BACKGROUND_GAME_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
spaceship_sprite = pg.transform.scale(pg.image.load(constants.PLAYER_SPRITE_PATH).convert_alpha(), (150, 50))
ball_sprite = pg.transform.scale(pg.image.load(constants.BALL_SPRITE_PATH).convert_alpha(), (20, 20))
brick_sprite = pg.transform.scale(pg.image.load(constants.BRICK_SPRITE_PATH).convert_alpha(), (70, 30))

# --------------------- contenedores Botones del menú -------------------

start_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 , 250, 80)
ranking_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 100, 250, 80)
exit_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 100, 250, 80)


#  --------------------- ladrillos ---------------------

brick_width, block_height = brick_sprite.get_size()
brick_space = 5
brick_rows = 5
brick_columns = 18

ladrillos = []
inicio_x = (constants.DISPLAY_WIDTH // 2) - (brick_columns * (brick_width + brick_space)) // 2
for fila in range(brick_rows):
    for col in range(brick_columns):
        ladrillo_x = inicio_x + col * (brick_width + brick_space)
        ladrillo_y = 50 + fila * (block_height + brick_space)
        ladrillos.append(brick_sprite.get_rect(topleft=(ladrillo_x, ladrillo_y)))

# --------------------- pelotita ---------------------

PELOTA_RADIO = 8
pelota_x = constants.DISPLAY_WIDTH // 2
pelota_y = constants.DISPLAY_HEIGTH // 2
pelota_dx = 5 # Velocidad en x
pelota_dy = -5 # Velocidad en y

pelota_rect = pg.Rect(pelota_x - PELOTA_RADIO, pelota_y - PELOTA_RADIO, 
                          PELOTA_RADIO * 2, PELOTA_RADIO * 2)

 # --------------------- cargar y escalar la imagen del botón --------------------- 

menu_button = pg.image.load(constants.MENU_BUTTON_PATH).convert_alpha()
menu_button = pg.transform.scale(menu_button, (constants.DISPLAY_WIDTH // 3 - 180, constants.DISPLAY_HEIGTH // 2 - 290))

# --------------------- Textos de los botones ---------------------

text_start_button = button_font.render("Start", True, (190,190,190))
text_exit_button = button_font.render("Exit", True, (190,190,190))
text_ranking_button = button_font.render("ranking", True, (190,190,190))

# --------------------- posicion inicial nave ---------------------
character_sprite_rect = spaceship_sprite.get_rect(center=(constants.DISPLAY_WIDTH // 2,constants.DISPLAY_HEIGTH // 2 + 320))

# pantalla del juego
def game():

    global pelota_dx, pelota_dy, ladrillos, playing # Acceso a variables globales
    
    # Limitar la nave a los bordes de la pantalla
    character_sprite_rect.x = max(0, character_sprite_rect.x)
    character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)

    # 
    # 1.  Movimiento de la Pelota
    pelota_rect.x += pelota_dx
    pelota_rect.y += pelota_dy
    
    
    # Colisión Izquierda
    if pelota_rect.left <= 0:
        pelota_dx = abs(pelota_dx) # Fuerza el rebote hacia la derecha
        pelota_rect.left = 0       # Corrige la posición
    # Colisión Derecha
    elif pelota_rect.right >= constants.DISPLAY_WIDTH:
        pelota_dx = -abs(pelota_dx) # Fuerza el rebote hacia la izquierda
        pelota_rect.right = constants.DISPLAY_WIDTH # Corrige la posición
    # Colisión Superior
    if pelota_rect.top <= 0:
        pelota_dy = abs(pelota_dy) # Fuerza el rebote hacia abajo
        pelota_rect.top = 0      # Corrige la posición
        
    # B. Colisión Pelota con la Nave (Pala)
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
        
    # 4. Condiciones de Fin de Juego (Perder y Ganar)
    
    # Perder: Si la pelota cae por debajo de la nave (Game Over)
    if pelota_rect.bottom >= constants.DISPLAY_HEIGTH:
        playing = False
        print("¡GAME OVER!")
        # Aquí podrías añadir una pantalla de Game Over

    # Ganar: Si no quedan ladrillos
    if not ladrillos:
        playing = False
        print("¡VICTORIA!")
        # Aquí podrías añadir una pantalla de Victoria
    
    # 5. Dibujo (Renderizado)
    screen.blit(background_game, (0, 0))

    # Dibujar Ladrillos
    for ladrillo in ladrillos:
        screen.blit(brick_sprite, ladrillo)

    # Dibujar Nave (Pala)
    screen.blit(spaceship_sprite, character_sprite_rect)

    # Dibujar Pelota (usamos el centro del Rect para el círculo)
    screen.blit(ball_sprite, (pelota_rect.x, pelota_rect.y))


    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        character_sprite_rect.x = max(0, character_sprite_rect.x)
        character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)
        character_sprite_rect.x -= 7
    if keys[pg.K_RIGHT]:
        character_sprite_rect.x = max(0, character_sprite_rect.x)
        character_sprite_rect.x = min(constants.DISPLAY_WIDTH - character_sprite_rect.width, character_sprite_rect.x)
        character_sprite_rect.x += 7

        

def main():
    clock = pg.time.Clock()
    # variable para controlar el bucle principal
    run = True
    mostra_menu = True
    introducction = True
    game_music_playing = False
    intro_music_playing = False

    pg.mixer.music.load(constants.MENU_MUSIC_PATH)
    pg.mixer.music.play(1)

    while run:
        
        clock.tick(60)  # Limitar a 60 FPS

        # entrega la lista de eventos que pueden ocurrir en el juego
        for event in pg.event.get():
            # si el tipo de evento coincide con el evento de salir
            if event.type == pg.QUIT:
                run = False # Salir del juego   

            elif event.type == pg.MOUSEBUTTONDOWN and mostra_menu:
                mouse_pos = pg.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    pg.mixer.music.stop()
                    mostra_menu = False # Iniciar el juego
                elif exit_button.collidepoint(mouse_pos):
                    run = False # Salir del juego 
        
        if mostra_menu:
            main_menu.draw_menu(screen,background_menu, title_font, border_font, menu_button, text_start_button, text_exit_button, text_ranking_button,start_button, exit_button, ranking_button)
        
        else:
      
            if introducction and not intro_music_playing:
                pg.mixer.music.load(constants.INTRO_MUSIC_PATH)
                pg.mixer.music.play(-1)     
                introduction.introduction(screen, background_introduction, gral_text_font)
                introducction = False
                
            
            else:
                if not game_music_playing:
                    pg.mixer.music.load(constants.GAME_MUSIC_PATH)
                    pg.mixer.music.play(-1)  
                    game_music_playing = True
                
                game()

        # actualiza la pantalla
        pg.display.flip()


main()
pg.quit()
sys.exit()
    