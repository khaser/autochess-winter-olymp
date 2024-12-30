from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from . import models as battle_models

def details(request, battle_id, turn):
    battle_turn_view = get_object_or_404(Battle, pk=battle_id)

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
