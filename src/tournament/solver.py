from random import shuffle

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
