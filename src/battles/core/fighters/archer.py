import random
from fighters.unit import Unit


class Archer(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "archer"
        super().__init__(x, y, 5, 4, 7, team)

    def type(self):
        return "a"
        #return self.health_points

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return max(adx, ady) <= 2 and self.team != fighter.team and fighter.is_alive()

