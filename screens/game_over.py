import pygame as pg
import sys
import ranking
import Utils.constants as cons

def game_over(screen, text_font, title_font, score, game_over_screen=True):

   title_text = "¡¡ GAME OVER !!"
   score_text = f"Tu puntuación: {score}"
   input_prompt = "Introduce tu nombre:"
   continue_text = "Pulsa ENTER para guardar | ESC para salir"

   input_box = pg.Rect(screen.get_width() // 2 + 30 , 350, 200, 40)
   player_name = ''
   active = True # La caja de entrada empieza activa
   score_saved = False # Indicador de si el puntaje ya fue guardado

   while game_over_screen:
      ranking.load_ranking()

      for event in pg.event.get():
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()

            
            if event.type == pg.MOUSEBUTTONDOWN:
                # Si el usuario hace clic en la caja, la activa
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            
            

            if event.type == pg.KEYDOWN:
                    
               if event.key == pg.K_RETURN:
                     # Lógica para guardar la puntuación
                  if player_name and not score_saved:
                        ranking.add_score(player_name, score)
                        score_saved = True # Marca como guardado
                        print(f"Puntuación de {player_name} ({score}) guardada.")
                        active = False 

               elif event.key == pg.K_BACKSPACE:
                  player_name = player_name[:-1] # slicing del ultimo caracter
                    
               elif event.key == pg.K_ESCAPE:
                  pg.quit()
                  sys.exit()
                    
               else:
                  # Limitar la longitud del nombre y aceptar solo caracteres alfanuméricos y espacios
                  if len(player_name) < 15 and event.unicode.isalnum() or event.unicode == ' ':
                        player_name += event.unicode
            

      # activar color de la caja
      box_color = cons.LIGHT_BLUE if active else cons.GRAY

      screen.fill((0, 0, 0))

      # Dibujar título, puntuación y mensaje de entrada
      rendered_title = title_font.render(title_text, True, cons.RED)
      screen.blit(rendered_title, (screen.get_width() // 2 - rendered_title.get_width() // 2, 100))

      rendered_score = text_font.render(score_text, True, (255, 255, 255))
      screen.blit(rendered_score, (screen.get_width() // 2 - rendered_score.get_width() // 2, 250))

      # Dibujar mensaje "Introduce tu nombre:"
      prompt_surf = text_font.render(input_prompt, True, (255, 255, 255))
      screen.blit(prompt_surf, (input_box.x - 510 , input_box.y + 10))

      # Dibujar la caja de entrada de texto
      txt_surface = text_font.render(player_name, True, (255, 255, 255))
      # Ajustar el ancho de la caja si el texto es muy largo
      width = max(200, txt_surface.get_width() + 10)
      input_box.w = width
        
      # Blit (Dibujar) el texto en la caja
      screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

      # Dibujar el rectángulo de la caja
      
      pg.draw.rect(screen, box_color, input_box, 2)

      # Dibujar mensaje de continuación
      if not score_saved:
            continue_surf = text_font.render(continue_text, True, (200, 200, 200))
      else:
            continue_surf = text_font.render("Puntuación guardada. Pulsa ESC para salir.", True, (0, 255, 0)) # Verde si se guardó

      screen.blit(continue_surf, (screen.get_width() // 2 - continue_surf.get_width() // 2, input_box.y + 220))
      

      pg.display.flip()
    