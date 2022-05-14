import calendar
import pprint

import numpy as np
import pandas as pd

performance = np.array([
    [0.3, 0, 0.4, 0.2, 0.05, 0.05],
    [0.3, 0, 0.125, 0.325, 0.2, 0.05],
    [0.25, 0, 0, 0.05, 0.5, 0.2],
    [0.15, 0, 0, 0.025, 0.175, 0.65],
])
presence = [
    (0.4, 0.6),
    (0.15, 0.85)
]


def adapter_calendar(new_calendar: list, old_calendar: list):
    for i in range(len(old_calendar)):
        if type(old_calendar[0]) == list:
            adapter_calendar(new_calendar, old_calendar[i])
        else:
            new_calendar.extend(old_calendar)
            return new_calendar
    return new_calendar


def stupid_adapter(new_calendar, old_calendar):
    for season in old_calendar:
        for month in season:
            for week in month:
                new_calendar += week
    return new_calendar


def main_loop():
    global performance
    students_count = 15
    cal = calendar.Calendar().yeardatescalendar(2021)
    cal = stupid_adapter([], cal)
    days = len(cal)
    key = ['date', 'name', 'presence', 'mathematics', 'physics', 'chemistry', 'english']
    name = [var for var in range(students_count)] * len(cal)
    cal = [val for val in cal for _ in range(0, students_count)]

    obj = ['mathematics', 'physics', 'chemistry', 'english']
    # students = dict.fromkeys(range(students_count), dict.fromkeys(obj, None).copy())
    students = {i: dict.fromkeys(obj, []) for i in range(students_count)}
    pprint.pprint(students)
    for st in students.keys():
        for o in students[st].keys():
            p = performance[np.random.choice(len(performance), size=1)]
            mark = np.random.choice(range(6), size=len(cal),
                                               p=list(p)[0])
            students[st][o] = mark

    data = dict.fromkeys(key, [0 for i in range(len(cal))])
    data["date"] = cal
    data["name"] = name
    for o in obj:
        data[o] = []
        for d in range(days):
            for st in students.keys():
                data[o].append(students[st][o][d])

    with open('passwd.csv', 'w', newline='') as f:
        df = pd.DataFrame(data)
        df.to_csv(path_or_buf=f, index=False)


def get_mean(lst: list):
    mean = 0
    count = 0
    for var in lst:
        if var != 0:
            mean += var
            count += 1
    return mean / count


if __name__ == '__main__':
    main_loop()
    df = pd.read_csv("passwd.csv")
    print(df)
    df = df.replace(0, None)
