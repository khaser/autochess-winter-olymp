from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from . import models as battle_models
from .core.game import fight

def details(request, battle_id, turn):

    red_fighters, blue_fighters = [
          {"fighter_kind": "archer", "x": 3, "y": 1},
          {"fighter_kind": "berserker", "x": 3, "y": 3},
          {"fighter_kind": "cavalry", "x": 4, "y": 2},
    ], [
          {"fighter_kind": "berserker", "x": 3, "y": 1},
          {"fighter_kind": "cavalry", "x": 4, "y": 1},
          {"fighter_kind": "berserker", "x": 5, "y": 1},
    ]
    
    # TODO NOW random_seed is equal to 1 maybe fix that
    red_fighters, blue_fighters, turn_arrows = fight(red_fighters, blue_fighters, turn, 1)

    print("hui", turn_arrows)

    return render(request, "battles/details.html", {
        'battle_id': battle_id,
        'turn': turn,
        'red_fighters': red_fighters,
        'blue_fighters': blue_fighters,
        'arrows': turn_arrows,
        'indexes8': list(range(8)),
        'steps': [-5, -1, 1, 5]
    })

@login_required
def index(request):
    # request.user is a django.auth user

    battles = []
    for battle in battle_models.Battle.objects.all():
        battles.append({
            'battle_id': battle.pk,
            'time': battle.time,
            'red_username': battle.red_username(),
            'blue_username': battle.blue_username(),
            'winner_username': battle.winner_username(),
        })

    return render(request, 'battles/index.html', {
        'battles': battles
    })
