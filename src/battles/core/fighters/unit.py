import random
import collections

class Unit():
    def __init__(self, x, y, hp, ap, ip, team):
        self.pos = [x, y]

        self.hp = hp
        self.ap = ap
        self.ip = ip

        self.team = team
    
    def __lt__(self, other):
        return self.ip > other.ip

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return f"(pos: {self.pos}; health: {self.hp})"

    def is_alive(self):
        return self.hp > 0

    def can_attack_enemy(self, fighter):
        return False

    def can_attack(self, fighters):
        for fighter in fighters:
            if self != fighter and self.can_attack_enemy(fighter):
                return True
        return False

    def attack(self, fighters, arrows, attackable):
        fighters[attackable].hp -= self.ap
        arrows.append((self.pos, fighters[attackable].pos))

    def perform_attack_phase(self, fighters, arrows):
        attackable_fighters = []
        for i in range(len(fighters)):
            if self != fighters[i] and self.can_attack_enemy(fighters[i]):
                attackable_fighters.append(i)
        choosen = random.choice(attackable_fighters)
        self.attack(fighters, arrows, choosen)
        return not fighters[choosen].is_alive()

    def perform_move_phase(self, fighters, arrows, table):
        to_nearest = self.get_move(fighters, table)
        arrows.append((self.pos, to_nearest))
        self.pos = to_nearest

    def perform_turn(self, fighters, arrows, table):
        if self.can_attack(fighters):
            self.perform_attack_phase(fighters, arrows)
        else:
            self.perform_move_phase(fighters, arrows, table)

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
                if blocked[next_pos[0]][next_pos[1]] == self.team:
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

