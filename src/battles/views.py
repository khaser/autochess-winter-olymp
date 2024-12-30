from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from ejudge.models import Contest
from ejudge.database import EjudgeDatabase, RunStatus
from django.conf import settings

from . import models as battle_models
from .core.game import fight
from users import models as user_models

@login_required
def details(request, battle_id, turn):

    user = request.user.info

    red_db_fighters = battle_models.get_user_fighters(user)
    red_fighters = [db_fighter.map_fighter() for db_fighter in red_db_fighters]

    blue_db_fighters = battle_models.get_user_fighters(user)
    blue_fighters = [db_fighter.map_fighter() for db_fighter in blue_db_fighters]

    # TODO NOW random_seed is equal to 1 maybe fix that
    red_fighters, blue_fighters, turn_arrows = fight(red_fighters, blue_fighters, turn, 1)

    return render(request, "battles/details.html", {
        'battle_id': battle_id,
        'turn': turn,
        'red_fighters': red_fighters,
        'blue_fighters': blue_fighters,
        'arrows': turn_arrows,
        'indexes8': list(range(8)),
        'steps': [-5, -1, 1, 5]
    })

# TODO: rewrite with generic.ListView
@login_required
def index(request):
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


@login_required
@csrf_exempt
def planning(request):
    user = request.user.info
    plc = user.get_cur_placement()

    if request.method == 'POST':
        match request.body.split():
            case (row, column, task):
                return post_fighter(row, column, task.decode('ascii'), user)
            case _:
                return HttpResponseBadRequest("invalid number of arguments")

    elif request.method == 'GET':
        unplaced_fighters = [
            { "shortname": "A", "fighter_kind" : "cavalry", "hp" : "13"},
            { "shortname": "B", "fighter_kind" : "knight", "hp" : "15"},
            { "shortname": "C", "fighter_kind" : "archer", "hp" : "5"}
        ]
        placed_fighters = [
            { "shortname": "D", "fighter_kind" : "cavalry", "hp" : "13", "x" : 6, "y" : 6},
            { "shortname": "E", "fighter_kind" : "knight", "hp" : "15", "x" : 6, "y" : 7},
            { "shortname": "F", "fighter_kind" : "archer", "hp" : "5", "x" : 5, "y" : 7}
        ]


        for fighter in plc.positionedfigher_set.all():
            # TODO
            # fighters.append()
            pass

        indexes8 = list(range(8))

        return render(request, 'battles/planning.html', {
            'unplaced_fighters': unplaced_fighters,
            'placed_fighters': placed_fighters,
            'indexes8': indexes8
        })


def post_fighter(row, column, task_sn, user):
    try:
        row = int(row)
        column = int(column)
    except:
        return HttpResponseBadRequest("Row or column can't be parsed as int")

    if not (5 < column < 8 and 0 <= row < 8):
        return HttpResponseBadRequest("Coordinates violates accepted range")
    # check task is solved
    if not check_task_is_solved(task_sn, user):
        return HttpResponseBadRequest("Task is not solved")

    if len(battle_models.PositionedFigher.objects.filter(row=row, column=column)):
        return HttpResponseBadRequest("Cell is already taken")

    plc = user.get_cur_placement()
    try:
        pos_fighter = plc.positionedfigher_set.get(fighter__ejudge_short_name=task_sn)
    except:
        fighter = battle_models.Fighter.objects.get(ejudge_short_name=task_sn)
        battle_models.PositionedFigher.create(
                    fighter=fighter,
                    row=row,
                    column=column,
                    placement=plc,
                  )
    return HttpResponse("ok")


def check_task_is_solved(task, user_info):
    contest = Contest(settings.EJUDGE_SERVE_CFG)
    ejudge_database = EjudgeDatabase()
    for run in ejudge_database.get_runs_by_user(user_info.user):
        short_name = contest.problems[run.problem_id].short_name
        if task == short_name and run.status == RunStatus.OK:
            return True
    return False

