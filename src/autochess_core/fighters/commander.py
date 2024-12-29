import random
import collections
from fighters.unit import Unit

class Commander(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "commander"
        super().__init__(x, y, 8, 3, 6, team)

    def type(self):
        return "l" # leader (c - fpr cavalry)
        #return self.health_points

    def can_attack_by_ally(self, ally, fighters):
        adx, ady = abs(self.pos[0] - ally.pos[0]), abs(self.pos[1] - ally.pos[1])
        return max(adx, ady) <= 1 and self.team == ally.team and ally.is_alive() and ally.can_attack(fighters)

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return max(adx, ady) <= 1 and self.team != fighter.team and fighter.is_alive()

    def can_attack(self, fighters):
        for fighter in fighters:
            if self != fighter and self.can_attack_enemy(fighter):
                return True
        for ally in fighters:
            if self != ally and self.can_attack_by_ally(ally, fighters):
                return True
        return False

    def perform_attack_phase(self, fighters, arrows):
        supported_allies = []
        for i in range(len(fighters)):
            if self != fighters[i] and self.can_attack_by_ally(fighters[i], fighters):
                supported_allies.append(i)
        if len(supported_allies) != 0:
            choosen_ally = random.choice(supported_allies)
            arrows.append((self.pos, fighters[choosen_ally].pos))
            killed = fighters[choosen_ally].perform_attack_phase(fighters, arrows)
            return killed

        # if can not trigger our ally
        attackable_fighters = []
        for i in range(len(fighters)):
            if self != fighters[i] and self.can_attack_enemy(fighters[i]):
                attackable_fighters.append(i)
        choosen = random.choice(attackable_fighters)
        self.attack(fighters, arrows, choosen)
        return not fighters[choosen].is_alive()

    def get_move(self, fighters, table):
        blocked = [[-1 for j in range(table.columns)] for i in range(table.rows)]
        parent = [[[-1, -1] for j in range(table.columns)] for i in range(table.rows)]
        parent[self.pos[0]][self.pos[1]] = self.pos
       
        for fighter in fighters:
            blocked[fighter.pos[0]][fighter.pos[1]] = fighter.team
        blocked[self.pos[0]][self.pos[1]] = -1

        directions = [[0, 1], [0, -1], [1, 0], [-1, 0],
                      [1, 1], [1, -1], [-1, 1], [-1, -1]]

        q = collections.deque()
        q.append(self.pos)

        path = collections.deque()
        
        while len(q) > 0:
            current = q.popleft()

            if blocked[current[0]][current[1]] != -1:
                path.append(current)
                break

            for direction in directions:
                next_pos = [current[0] + direction[0], current[1] + direction[1]]
                if not table.into(next_pos):
                    continue
                if parent[next_pos[0]][next_pos[1]] != [-1, -1]:
                    continue
                parent[next_pos[0]][next_pos[1]] = current
                q.append(next_pos)

        if len(path) == 0:
            return self.pos

        while path[-1] != parent[path[-1][0]][path[-1][1]]:
            path.append(parent[path[-1][0]][path[-1][1]])
            if len(path) > 2:
                path.popleft()

        return path[0]

