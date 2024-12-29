import random
import time


from fighters.infantryman import Infantryman
from fighters.knight import Knight
from fighters.archer import Archer
from fighters.berserker import Berserker
from fighters.cavalry import Cavalry
from fighters.guardsman import Guardsman
from fighters.commander import Commander


class Table():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def into(self, coords):
        return 0 <= coords[0] and coords[0] < self.rows and 0 <= coords[1] and coords[1] < self.columns


class Game():
    def __init__(self, teams_metas, table, seed):
        random.seed(seed)

        self.turn = 0
        self.table = table
        self.teams = len(teams_metas)
        self.arrows = []

        team_fighters = []
        for i in range(len(teams_metas)):
            team_fighters.append(self.extract_fighters_from_metas(teams_metas[i], i))

        self.fighters = self.prepare_fighters(team_fighters)

    def extract_fighter_from_meta(self, meta, team_number):
        match meta["fighter_kind"]:
            case "infantryman":
                return Infantryman(meta["x"], meta["y"], team_number)
            case "knight":
                return Knight(meta["x"], meta["y"], team_number)
            case "archer":
                return Archer(meta["x"], meta["y"], team_number)
            case "berserker":
                return Berserker(meta["x"], meta["y"], team_number)
            case "cavalry":
                return Cavalry(meta["x"], meta["y"], team_number)
            case "commander":
                return Commander(meta["x"], meta["y"], team_number)
            case "guardsman":
                return Guardsman(meta["x"], meta["y"], team_number)
            case _:
                return None

    def extract_fighters_from_metas(self, metas, team_number):
        fighters = []
        for meta in metas:
            fighters.append(self.extract_fighter_from_meta(meta, team_number))
        return fighters

    def prepare_fighters(self, team_fighters):
        # unite + shuffle + initiative sort
        fighters = []
        for i in range(len(team_fighters)):
            fighters += team_fighters[i]
        random.shuffle(fighters)
        fighters.sort()

        return fighters

    def clear_table(self):
        for i in range(len(self.fighters) - 1, -1, -1):
            if not self.fighters[i].is_alive():
                self.fighters.pop(i)

    def make_turn(self):
        # clear arrows from previous turn
        self.arrows = []
        current_fighter = self.fighters[self.turn]
        
        # make turn by fighter
        current_fighter.perform_turn(self.fighters, self.arrows, self.table)
        self.clear_table()
        self.turn = (self.turn + 1) % len(self.fighters)

    def is_finished(self):
        alive_teams = set()
        for fighter in self.fighters:
            alive_teams.add(fighter.team)
        return len(alive_teams) <= 1

    def print(self):
        print_data = [["*" for i in range(self.table.columns)] for j in range(self.table.rows)] 
        for fighter in self.fighters:
            mtype = fighter.type()
            if fighter.team == 1:
                mtype = mtype.upper()
            print_data[fighter.pos[0]][fighter.pos[1]] = mtype
            print(mtype, fighter)
        for i in range(len(print_data)):
            for j in range(len(print_data[i])):
                print(print_data[i][j], end='')
            print()

    def extract_arrows(self):
        return self.arrows

    def extract_meta_from_fighter(self, fighter):
        meta = dict()
        meta["x"] = fighter.pos[0]
        meta["y"] = fighter.pos[1]
        meta["fighter_kind"] = fighter.fighter_kind
        return meta

    def extract_metas_from_fighters(self):
        team_fighters = [[] for i in range(self.teams)]
        for fighter in self.fighters:
            team_fighters[fighter.team].append(self.extract_meta_from_fighter(fighter))
        return team_fighters


def rotate_vertical(meta, table_size):
    meta["y"] = table_size[1] - meta["y"] - 1


def rotate_all_vertical(metas, table_size):
    for meta in metas:
        rotate_vertical(meta, table_size)


def prepare_metas(metas):
    for meta in metas:
        meta["x"] = int(meta["x"])
        meta["y"] = int(meta["y"])


def fight(a_fighters, b_fighters, turns, random_seed):
    prepare_metas(a_fighters)
    prepare_metas(b_fighters)

    rotate_all_vertical(b_fighters, (8, 8))

    current_game = Game([a_fighters, b_fighters], Table(8, 8), random_seed)
    # run turns emulation
    for _ in range(turns):
        current_game.make_turn()
        if current_game.is_finished():
            break
    # get actual info about game 
    fighters = current_game.extract_metas_from_fighters()
    lst_arrows = current_game.extract_arrows()
    # return actual info
    return (fighters[0], fighters[1], lst_arrows)

