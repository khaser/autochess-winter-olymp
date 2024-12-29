import random
from fighters.unit import Unit


class Berserker(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "berserker"
        super().__init__(x, y, 9, 3, 9, team)

    def type(self):
        return "b"
        #return self.health_points

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return max(adx, ady) <= 1 and self.team != fighter.team and fighter.is_alive()

    def perform_turn(self, fighters, arrows, table_size):
        if self.can_attack(fighters):
            killed = self.perform_attack_phase(fighters, arrows)
            while killed and self.can_attack(fighters):
                killed = self.perform_attack_phase(fighters, arrows)
        else:
            self.perform_move_phase(fighters, arrows, table_size)

