import json
import os
from datetime import datetime

RANKING_FILE = "ranking.json"

def get_score(ranking):
    return ranking['score']

def sort_and_limit_ranking(ranking):

    ranking.sort(key=get_score, reverse=True)
    return ranking[:5]


def load_ranking():
    """Carga el ranking desde JSON"""
    if os.path.exists(RANKING_FILE):
        try:
            with open(RANKING_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_ranking(ranking):
    """Guarda el ranking en JSON"""
    with open(RANKING_FILE, 'w') as f:
        json.dump(ranking, f, indent=4)

def add_score(name, score):
    
    ranking = load_ranking()
  
    ranking.append({
        'name': name,
        'score': score,
        'date': datetime.now().strftime("%d/%m/%Y %H:%M")
    })
   
    ranking = sort_and_limit_ranking(ranking) 
    save_ranking(ranking)
    return ranking

def get_ranking():
    """Obtiene el ranking actual"""
    return load_ranking()