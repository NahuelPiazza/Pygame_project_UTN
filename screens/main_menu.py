import pygame as pg
import constants
# pantalla de menu inicio

def draw_menu(screen, background_menu, title_font, border_font,
    menu_button, text_start_button, text_exit_button, text_ranking_button,
    start_button, exit_button, ranking_button,
    volume_on, volume_off, volume_button, is_volume_on):

    screen.blit(background_menu, (0, 0))

    # ---- TÍTULO ----
    title_text = title_font.render("Galaxnoid", True, constants.WHITE)
    borde_surf = border_font.render("Galaxnoid", True, constants.BLACK)

    title_x = screen.get_width() // 2
    title_y = screen.get_height() // 2 - 200

    # borde del título
    borde_rect = borde_surf.get_rect(center=(title_x + 5, title_y + 5))
    screen.blit(borde_surf, borde_rect)

    # título
    title_rect = title_text.get_rect(center=(title_x, title_y))
    screen.blit(title_text, title_rect)

    # ---- AJUSTAR TAMAÑO DEL BOTÓN ----
    # <<< ACA AJUSTÁS EL TAMAÑO >>>
    menu_button_scaled = pg.transform.scale(menu_button, (320, 110))
    # Cambiá 320, 110 por el tamaño que vos quieras

    # ---- CENTRAR BOTONES ----
    center_x = screen.get_width() // 2 - menu_button_scaled.get_width() // 2

    # POSICIONES DEL FONDO DEL BOTÓN
    start_y   = screen.get_height() // 2 - 40
    ranking_y = screen.get_height() // 2 + 90
    exit_y    = screen.get_height() // 2 + 220

    # Dibujar fondo de cada botón
    screen.blit(menu_button_scaled, (center_x, start_y))
    screen.blit(menu_button_scaled, (center_x, ranking_y))
    screen.blit(menu_button_scaled, (center_x, exit_y))

    # ---- BOTÓN DE VOLUMEN ----
    if is_volume_on:
        screen.blit(volume_on, (volume_button.x, volume_button.y))
    else:
        screen.blit(volume_off, (volume_button.x, volume_button.y))

    # ---- TEXTO CENTRADO ----
    # CENTRAMOS USANDO EL TAMAÑO NUEVO DEL BOTÓN
    bw = menu_button_scaled.get_width()
    bh = menu_button_scaled.get_height()

    # START
    sx = center_x + (bw - text_start_button.get_width()) // 2
    sy = start_y + (bh - text_start_button.get_height()) // 2
    screen.blit(text_start_button, (sx, sy))

    # RANKING
    rx = center_x + (bw - text_ranking_button.get_width()) // 2
    ry = ranking_y + (bh - text_ranking_button.get_height()) // 2
    screen.blit(text_ranking_button, (rx, ry))

    # EXIT
    ex = center_x + (bw - text_exit_button.get_width()) // 2
    ey = exit_y + (bh - text_exit_button.get_height()) // 2
    screen.blit(text_exit_button, (ex, ey))