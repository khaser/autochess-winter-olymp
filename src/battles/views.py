from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from ejudge.models import Contest
from ejudge.database import EjudgeDatabase, RunStatus
from django.conf import settings

from . import models as battle_models
from .core.game import fight
from users import models as user_models

import math

@login_required
def details_neg(request, battle_id, turn):
    return redirect('battles:details', battle_id=battle_id, turn=0)

def details(request, battle_id, turn):

    battle = battle_models.Battle.objects.get(pk=battle_id)

    red_db_fighters = battle_models.get_placement_fighters(battle.red_placement)
    red_fighters = [db_fighter.map_fighter() for db_fighter in red_db_fighters]

    blue_db_fighters = battle_models.get_placement_fighters(battle.blue_placement)
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


def scores(request):

    uscores = []
    for user_info in user_models.UserInfo.objects.all():
        uscores.append((calculate_score(user_info), user_info))

    uscores.sort(key=lambda x: x[0], reverse=True)

    results = []
    for place, (score, user_info) in enumerate(uscores):
        results.append({
            "place": place + 1,
            "name": user_info.get_login(),
            "score": score,
        })

    return render(request, 'battles/scores.html', {
        'results': results
    })


def calculate_score(user_info):
    res = 0
    for placement in battle_models.Placement.objects.filter(user=user_info).all():
        def helper(battle):
            return math.sqrt((battle.time.replace(tzinfo=None) -
                        settings.CONTEST_START_TIME.replace(tzinfo=None)).seconds // 60)
        try:
            battle = placement.battles_as_blue
            if battle.result == battle_models.BattleResult.BLUE:
                res += helper(battle)
        except battle_models.Placement.battles_as_blue.RelatedObjectDoesNotExist:
            pass

        try:
            import datetime as dt
            battle = placement.battles_as_red
            if battle.result == battle_models.BattleResult.RED:
                res += helper(battle)
        except battle_models.Placement.battles_as_red.RelatedObjectDoesNotExist:
            pass
    return res

@login_required
@csrf_exempt
def planning(request):
    user = request.user.info
    plc = user.get_cur_placement()

    if request.method == 'POST':
        match request.body.split():
            case (row, column, task):
                return post_fighter(row, column, task.decode('ascii'), user)
            case (task,):
                return retire_fighter(task.decode('ascii'), user)
            case _:
                return HttpResponseBadRequest("invalid number of arguments")

    elif request.method == 'GET':
        unplaced_fighters = []
        placed_fighters = []

        placed_tasks = set()

        for fighter in plc.positionedfigher_set.all():
            shortname = fighter.fighter.ejudge_short_name
            placed_fighters.append({
                'shortname': shortname,
                'fighter_kind': fighter.fighter.kind,
                'hp': fighter.fighter.getHp(),
                'x': fighter.row,
                'y': fighter.column,
            })
            placed_tasks.add(shortname)

        for fighter in battle_models.Fighter.objects.all():
            if check_task_is_solved(fighter.ejudge_short_name, user) and \
                    fighter.ejudge_short_name not in placed_tasks:
                unplaced_fighters.append({
                    'shortname': fighter.ejudge_short_name,
                    'fighter_kind': fighter.kind,
                    'hp': fighter.getHp(),
                })

        indexes8 = list(range(8))

        return render(request, 'battles/planning.html', {
            'unplaced_fighters': unplaced_fighters,
            'placed_fighters': placed_fighters,
            'indexes8': indexes8
        })

def lore(request):

        return render(request, 'battles/rules/lore.html', {

        })

def combat(request):

        return render(request, 'battles/rules/combat.html', {

        })

def monsters(request):

        return render(request, 'battles/rules/monsters.html', {

        })

def retire_fighter(task_sn, user):
    fighter_to_rem = user.get_cur_placement().positionedfigher_set.filter(fighter__ejudge_short_name=task_sn).all()
    assert len(fighter_to_rem) < 2
    if len(fighter_to_rem) == 1:
        fighter_to_rem[0].delete()
        return HttpResponse("ok")
    else:
        return HttpResponseBadRequest("Fighter for this task haven't posted")


def post_fighter(row, column, task_sn, user):
    try:
        row = int(row)
        column = int(column)
    except:
        return HttpResponseBadRequest("Row or column can't be parsed as int")

    if not (5 <= column < 8 and 0 <= row < 8):
        return HttpResponseBadRequest("Coordinates violates accepted range")
    # check task is solved
    if not check_task_is_solved(task_sn, user):
        return HttpResponseBadRequest("Task is not solved")

    if len(battle_models.PositionedFigher.objects.filter(row=row, column=column)):
        return HttpResponseBadRequest("Cell is already taken")

    plc = user.get_cur_placement()
    try:
        pos_fighter = plc.positionedfigher_set.get(fighter__ejudge_short_name=task_sn)
        pos_fighter.column = column
        pos_fighter.row = row
        pos_fighter.save()
    except battle_models.PositionedFigher.DoesNotExist:
        fighter = battle_models.Fighter.objects.get(ejudge_short_name=task_sn)
        battle_models.PositionedFigher.objects.create(
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

