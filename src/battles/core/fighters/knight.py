import random
import collections 
from ..fighters.unit import Unit


class Knight(Unit):
    fighter_kind: str

    def __init__(self, x, y, team):
        self.fighter_kind = "knight"
        super().__init__(x, y, 15, 5, 8, team)

    def type(self):
        return "k"
        #return self.health_points

    def can_attack_enemy(self, fighter):
        adx, ady = abs(self.pos[0] - fighter.pos[0]), abs(self.pos[1] - fighter.pos[1])
        return (adx + ady) <= 1 and self.team != fighter.team and fighter.is_alive()

    def get_move(self, fighters, table):
        blocked = [[-1 for j in range(table.columns)] for i in range(table.rows)]
        parent = [[[-1, -1] for j in range(table.columns)] for i in range(table.rows)]
        parent[self.pos[0]][self.pos[1]] = self.pos
       
        for fighter in fighters:
            blocked[fighter.pos[0]][fighter.pos[1]] = fighter.team
        blocked[self.pos[0]][self.pos[1]] = -1

        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

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

