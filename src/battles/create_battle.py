from django.conf import settings

from users import models as user_models
from django.contrib.auth import models as auth_models
from . import models as battle_models

from .core import game

def create_battle(red_username, blue_username):
    red_plc = copy_user_placement(red_username)
    blue_plc = copy_user_placement(blue_username)

    battle = battle_models.Battle.objects.create(red_placement=red_plc,blue_placement=blue_plc)

    # TODO: generate seed and store to DB
    red_team = map_fighters(red_plc)
    blue_team = map_fighters(blue_plc)
    print(red_team)
    print(blue_team)
    (red_team_fin, blue_team_fin, _) = game.fight(red_team, blue_team, settings.TURNS_IN_ROUND_LIMIT, 1)

    if len(red_team_fin) > 0:
        battle.result = battle_models.BattleResult.RED
    elif len(blue_team_fin) > 0:
        battle.result = battle_models.BattleResult.BLUE
    else:
        raise f"Game not finished, fighters alive: (red: {len(red_team_fin)}, blue: {len(blue_team_fin)})"
    battle.save()

def copy_user_placement(username):
    user = user_models.UserInfo.objects.get(user__first_name=username)
    plc = user.placement_set.latest("pk")
    battle_plc_id = plc.id
    plc.id = None
    plc.save()

    prev_plc = user.placement_set.get(pk=battle_plc_id)
    for fighter in prev_plc.positionedfigher_set.all():
        fighter.placement = plc
        fighter.id = None
        fighter.save()

    return prev_plc

def map_fighters(plc):
    return [map_fighter(db_fighter) for db_fighter in plc.positionedfigher_set.all()]

def map_fighter(fighter):
    return {
            'x': fighter.column,
            'y': fighter.row,
            'fighter_kind': fighter.fighter.kind,
            }
