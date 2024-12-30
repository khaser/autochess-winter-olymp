from django.shortcuts import render

from django.contrib.auth.decorators import login_required

def details(request, battle_id, turn):
    battle_turn_view = get_object_or_404(Battle, pk=battle_id)
    template_name = "polls/detail.html"

@login_required
def index(request):
    # request.user is a django.auth user

    battles = [
        {'battle_id': 1, 'time': '17:30', 'red_username': 'kekeers', 'blue_username': 'lolers', 'winner_username': 'lolers'},
        {'battle_id': 2, 'time': '17:30', 'red_username': 'doters',  'blue_username': 'lolers', 'winner_username': 'doters'},
    ]

    return render(request, 'battles/index.html', {
        'battles': battles
    })

# def battle_turn_view(request, battle_id, turn):
#     battle_turn_view = get_object_or_404(Battle, pk=battle_id)
#     template_name = "polls/detail.html"
