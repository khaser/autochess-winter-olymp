from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import *

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
def planning(request):
    plc = request.user.get_cur_placement()

    # TODO: rewrite
    if request.method == 'POST':
        match request.body().split():
            case (row, column, task):
                return post_fighter(row, column, task, user)
            case _:
                return Http406("invalid number of arguments")

    elif request.method == 'GET':
        fighters = []

        for fighter in plc.positionedfigher_set.all():
            # TODO
            # fighters.append()
            pass

        return render(request, 'battles/planning.html', {
            'fighters': fighters
        })


def post_fighter(row, column, task_sn, user):
    try:
        row = int(row)
        column = int(column)
        if not (5 < column < 8 and 0 <= row < 8):
            return Http406
        # check task is solved
        if not check_task_is_solved(task_sn, user):
            return Http406

        if len(battle_models.PositionedFighter.filter(row=row, column=column)):
            return Http406

        plc = request.users.get_cur_placement()
        try:
            pos_fighter = plc.positionedfigher_set.get(fighter__ejudge_short_name=task_sn)
        except:
            fighter = battle_models.Fighters.get(ejudge_short_name=tasn_sn)
            battle_models.PositionedFighter.create(
                        fighter=fighter,
                        row=row,
                        column=y,
                        placement=plc,
                      )

    except:
        return Http406


def check_task_is_solved(task, user):
    contest = Contest(settings.EJUDGE_SERVE_CFG)
    ejudge_database = EjudgeDatabase()
    for run in ejudge_database.get_runs_by_user(user):
        if run.status == RunStatus.IGNORED:
            continue
        # We don't have tile for this ejudge problem
        if contest.problems[run.problem_id].short_name not in tiles_by_short_name:
            continue
        if run.status == RunStatus.OK:
            return True
    return False

