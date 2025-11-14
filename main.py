import pygame as pg
import sys
import constants

pg.init()

# seteamos ancho y alto de pantalla
screen = pg.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGTH), pg.RESIZABLE)

# colocamos el icono y titulo de la ventana
pg.display.set_icon(pg.image.load(constants.ICON_PATH).convert())
pg.display.set_caption("Bushi-Do!")

# Definir fuentes para los elementos
gral_text_font = pg.font.Font(constants.FONT_PATH, 25)
title_font = pg.font.Font(constants.FONT_PATH, 74)
border_font = pg.font.Font(constants.FONT_PATH, 75)
button_font = pg.font.Font(constants.FONT_PATH, 35)

# cargar y escalar la imagenes
background_menu = pg.transform.scale(pg.image.load(constants.BACKGROUND_MENU_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
background_introduction = pg.transform.scale(pg.image.load(constants.BACKGROUND_INTRO_PATH).convert(),(constants.DISPLAY_WIDTH,constants.DISPLAY_HEIGTH))
# contenedores Botones del menú
start_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 , 250, 80)
exit_button = pg.Rect(constants.DISPLAY_WIDTH // 2 - 110, constants.DISPLAY_HEIGTH // 2 + 100, 250, 80)

 # cargar y escalar la imagen del botón
menu_button = pg.image.load(constants.MENU_BUTTON_PATH).convert_alpha()
menu_button = pg.transform.scale(menu_button, (constants.DISPLAY_WIDTH // 3 - 170, constants.DISPLAY_HEIGTH // 2 - 150))

# Textos de los botones
text_start_button = button_font.render("Start", True, (190,190,190))
text_exit_button = button_font.render("Exit", True, (190,190,190))

# pantalla de menu inicio
def draw_menu():
    screen.blit(background_menu, (0, 0))
    
    # renderiza y dibuja el título del juego
    title_text = title_font.render("Bushi-Do", True, constants.WHITE)
    title_rect = title_text.get_rect()
    # sombreado del título
    borde_surf = border_font.render("Bushi-Do", True, constants.BLACK)
    borde_rect =title_rect.move((screen.get_width() // 2 - title_text.get_width() // 2 + 10, screen.get_height() // 2 - 200))

    #pegamos titulo y sombreado
    screen.blit(borde_surf, borde_rect)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2 + 5, screen.get_height() // 2 - 200))

    #colocamos imagen de boton
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 130, screen.get_height() // 2 - 80))
    screen.blit(menu_button, (screen.get_width() // 2 - title_text.get_width() // 2 + 130, screen.get_height() // 2 + 50))
    
    # dibuja el texto de los botones y los pega
    screen.blit(text_start_button, (start_button.x + (start_button.width - text_start_button.get_width()) // 2, start_button.y + (start_button.height - text_start_button.get_height()) // 2 ))
    screen.blit(text_exit_button, (exit_button.x + (exit_button.width - text_exit_button.get_width()) // 2, exit_button.y + (exit_button.height - text_exit_button.get_height()) // 2 + 30))

# pantalla de introduccion
def introduction():
    screen.blit(background_introduction, (0, 0))
    intro_text = gral_text_font.render("introduccion al juego...", True, constants.BLACK)
    screen.blit(intro_text, (screen.get_width() // 2 - intro_text.get_width() // 2, screen.get_height() // 2 - intro_text.get_height() // 2))
    pg.display.flip()
    pg.time.delay(5000)  # Pausa de 5 segundos para mostrar la introducción, hacer mecanica con un boton despues

# pantalla del juego
def game():
    pass
        

def main():
    clock = pg.time.Clock()
    # variable para controlar el bucle principal
    run = True

    position_x, position_y = 100, 100
    movement = (0, 0)
    mostra_menu = True
    introducction = True

    while run:
        
        clock.tick(60)  # Limitar a 60 FPS

        # entrega la lista de eventos que pueden ocurrir en el juego
        for event in pg.event.get():
            # si el tipo de evento coincide con el evento de salir
            if event.type == pg.QUIT:
                run = False
                # Salir del juego   

            elif event.type == pg.MOUSEBUTTONDOWN and mostra_menu:
                mouse_pos = pg.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    mostra_menu = False 
                     # Iniciar el juego
                elif exit_button.collidepoint(mouse_pos):
                    run = False 
                     # Salir del juego 

        if mostra_menu:
            draw_menu()
                            # pg.mixer.music.load(constants.MENU_MUSIC_PATH)
                            # pg.mixer.music.play(3)
        
        else:
      
            if introducction:    
                introduction()
                introducction = False
                
            
            else:
            # Lógica del juego (por ahora vacío)
                screen.fill(constants.BLACK)
                game_text = gral_text_font.render("Juego corriendo...", True, constants.WHITE)
                screen.blit(game_text, (screen.get_width() // 2 - game_text.get_width() // 2, screen.get_height() // 2 - game_text.get_height() // 2))

        # actualiza la pantalla
        pg.display.flip()


main()
pg.quit()
sys.exit()
    