import random
from fighters.unit import Unit


class Cavalry(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "cavalry"
        super().__init__(x, y, 13, 5, 12, team)

    def type(self):
        return "c"
        #return self.health_points

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return max(adx, ady) <= 1 and self.team != fighter.team and fighter.is_alive()

    def perform_attack_phase(self, fighters, arrows):
        attackable_fighters = []
        minimal_ip = -1
        for i in range(len(fighters)):
            if self != fighters[i] and self.can_attack_enemy(fighters[i]):
                attackable_fighters.append(i)
                if minimal_ip == -1:
                    minimal_ip = fighters[i].ip
                minimal_ip = min(minimal_ip, fighters[i].ip)
        for i in range(len(attackable_fighters) - 1, -1, -1):
            if fighters[attackable_fighters[i]].ip != minimal_ip:
                attackable_fighters.pop(i)
        choosen = random.choice(attackable_fighters)
        self.attack(fighters, arrows, choosen)
        return not fighters[choosen].is_alive()

    def perform_move_phase(self, fighters, arrows, table):
        jump_position = self.get_jump(fighters, table)
        if jump_position != None:
            arrows.append((self.pos, jump_position))
            self.pos = jump_position
            return
        to_nearest = self.get_move(fighters, table)
        arrows.append((self.pos, to_nearest))
        self.pos = to_nearest

    def get_jump(self, fighters, table):
        best_hdist = 0
        best_vdist = 0

        best_horizontal_jump = []
        best_vertical_jump = []

        blocked_positions = [[-1 for j in range(table.columns)] for i in range(table.rows)]
        for fighter in fighters:
            blocked_positions[fighter.pos[0]][fighter.pos[1]] = fighter.team

        # check horizontal jumps
        for y in range(0, table.columns):
            new_pos = [self.pos[0], y]
            if blocked_positions[new_pos[0]][new_pos[1]] != -1:
                continue
            
            # dirty hack check that it works properly
            future_cavalry = Cavalry(new_pos[0], new_pos[1], self.team)
            if future_cavalry.can_attack(fighters) and abs(y - self.pos[1]) > best_hdist: # at the same time we have current and future version of calvary
                best_horizontal_jump = new_pos
                best_hdist = abs(best_horizontal_jump[1] - self.pos[1])

        # check vertical jumps
        for x in range(0, table.rows):
            new_pos = [x, self.pos[1]]
            if blocked_positions[new_pos[0]][new_pos[1]] != -1:
                continue

            # dirty hack check that it works properly
            future_cavalry = Cavalry(new_pos[0], new_pos[1], self.team)
            if future_cavalry.can_attack(fighters) and abs(x - self.pos[0]) > best_vdist:
                best_vertical_jump = new_pos
                best_vdist = abs(best_vertical_jump[0] - self.pos[0])

        # check that jumps exist
        if len(best_horizontal_jump) == 0 and len(best_vertical_jump) == 0:
            return None

        if best_hdist >= best_vdist:
            return best_horizontal_jump
        return best_vertical_jump

