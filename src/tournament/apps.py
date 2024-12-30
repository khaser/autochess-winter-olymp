from django.apps import AppConfig
from django.conf import settings

from random import shuffle

import math, datetime

from apscheduler.schedulers.background import BackgroundScheduler

def create_battle_wrapper(red_team, blue_team):
    from battles.create_battle import create_battle
    return create_battle(red_team, blue_team)

class TournamentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tournament'

    def ready(self):

        rfreq = settings.ROUND_FREQ
        n_rounds = math.ceil((settings.CONTEST_DURATION) / rfreq)

        schedule = generate_schedule(settings.REGISTRED_TEAMS, n_rounds)

        scheduler = BackgroundScheduler()

        assert(len(schedule) == n_rounds)

        for round_id, sched_round in enumerate(schedule):
            for battle_in_round, (red_team, blue_team) in enumerate(sched_round):
                if red_team == None or blue_team == None:
                    # TODO
                    continue
                battle_time = settings.CONTEST_START_TIME + (round_id + 1) * settings.ROUND_FREQ + \
                                battle_in_round * datetime.timedelta(seconds=2)
                scheduler.add_job(create_battle_wrapper, 'date', args=[red_team, blue_team], run_date=battle_time)

        scheduler.start()

def generate_schedule(team_list, round_count):
    teams = team_list[:]
    n = len(teams)
    if n % 2 != 0:
        teams.append(None)
        n += 1
    result = []
    for shift in range(round_count):
        if shift % (n - 1) == 0 and shift != 0:
            shuffle(teams)
        round_result = []
        for i in range(n // 2):
            round_result.append([teams[i], teams[n - i - 1]])
        result.append(round_result)
        tmp = teams[1]
        teams[1] = teams[n - 1]
        for j in range(2, n):
            teams[j], tmp = tmp, teams[j]
    return result

