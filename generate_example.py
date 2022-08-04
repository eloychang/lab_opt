
import pandas as pd
import random

def generate_tasks(N):
    return pd.DataFrame({
        "ID" : [f"AA{i}" for i in range(N)],
        "area" : random.choices(["AE", "DS", "DT"],k = N),
        "objective" : random.choices([True, False], weights = [0.3, 0.7], k = N),
        "difficulty" : random.choices(list(range(1,11)), weights = list(range(10,0,-1)), k = N),
        "points" : [random.randint(1,10) for _ in range(N)]
    })


def generate_team_stats(tasks):
    team_stats = pd.DataFrame({
        "ID" : ["IB", "ML", "GA", "SB", "FP", "MM", "YO", "DA", "FS", "AF", "GV"],
        "area" : random.choices(["AE", "DS", "DT"], k = 11),
        "seniority" : random.choices(["In", "Jr", "Ssr", "Sr"],k = 11),
    })
    seniority = {
        "In" : 0,
        "Jr" : 1,
        "Ssr" : 2,
        "Sr" : 3
    }
    for _, task in tasks.iterrows():
        team_stats[f"time_to_task_{task.ID}"] = [random.gammavariate(8*max(1, task.difficulty - seniority[member.seniority]), 2) for _,member in team_stats.iterrows()]
    return team_stats