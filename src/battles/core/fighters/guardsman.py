import random
from fighters.unit import Unit


class Guardsman(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "guardsman"
        super().__init__(x, y, 14, 4, 10, team)

    def type(self):
        return "g"
        #return self.health_points

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return max(adx, ady) <= 1 and self.team != fighter.team and fighter.is_alive()

    def perform_turn(self, fighters, arrows, table_size):
        if self.can_attack(fighters):
            self.perform_attack_phase(fighters, arrows)
            # Guardsman attack property (second attack)
            if self.can_attack(fighters):
                self.perform_attack_phase(fighters, arrows)
        else:
            self.perform_move_phase(fighters, arrows, table_size)

