import pygame as pg

from ranking import get_ranking
import Utils.constants as constants


def draw_ranking(screen, title_font, gral_text_font):
    """Pantalla para mostrar el ranking"""
    ranking = get_ranking()
    screen.fill(constants.BLACK)
    
    title_text = title_font.render("TOP 5 SCORES", True, constants.LIGHT_BLUE)
    screen.blit(title_text, (constants.DISPLAY_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    
    if ranking:
        y_offset = 150
        for i, entry in enumerate(ranking, 1):
            rank_text = gral_text_font.render(f"{i}. {entry['name']}: {entry['score']}", True, constants.WHITE)
            screen.blit(rank_text, (constants.DISPLAY_WIDTH // 2 - rank_text.get_width() // 2, y_offset))
            y_offset += 60
    else:
        no_scores = gral_text_font.render("No hay scores aún", True, constants.WHITE)
        screen.blit(no_scores, (constants.DISPLAY_WIDTH // 2 - no_scores.get_width() // 2, 200))
    
    back_text = gral_text_font.render("Presiona SPACE para volver", True, constants.WHITE)
    screen.blit(back_text, (constants.DISPLAY_WIDTH // 2 - back_text.get_width() // 2, constants.DISPLAY_HEIGTH - 100))
    
    pg.display.flip()