# choose_robot.py - which kind of robot fits a job best? (a weighted score)
kinds = ["wheeled", "tracked", "legged", "flying"]

# How good each kind is (1 = bad, 5 = very good) at:
#          flat  stairs rough speed  time  cheap  load  safe near people
scores = [[5,    1,     2,    4,     5,    5,     4,    5],    # wheeled
          [4,    2,     4,    3,     4,    4,     5,    4],    # tracked
          [4,    5,     5,    2,     2,    1,     2,    3],    # legged
          [5,    5,     5,    5,     1,    3,     1,    1]]    # flying

# How important each point is for the job (0 = not at all, 5 = very important)
jobs = [["warehouse transport",     [5, 0, 0, 3, 5, 4, 5, 4]],
        ["plant with stairs",       [2, 5, 3, 1, 3, 1, 1, 3]],
        ["survey a big farm field", [1, 0, 3, 5, 3, 3, 0, 1]]]

for job in jobs:
    name = job[0]
    weights = job[1]
    print("Job:", name)
    for k in range(4):
        total = 0
        for c in range(8):
            total = total + scores[k][c] * weights[c]
        print("   ", kinds[k], total)
