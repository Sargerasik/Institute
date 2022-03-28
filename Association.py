import csv
import pandas as pd
import numpy as np


def main_loop():
    with open("Dataset.txt", 'r') as f:
        text = csv.reader(f, delimiter=" ")
        student = set()
        activity = set()
        for row in text:
            student.add(row[0])
            activity.add(row[1])
        student = list(map(str, sorted(list(map(int, student)))))
        activity = list(activity)
        data = [[0 for i in range(len(activity))] for i in range(len(student))]
        df = pd.DataFrame.from_records(data, index=student, columns=activity)
        f.seek(0)
        for row in text:
            df[row[1]][row[0]] += 1
        for i in df:
            print(i)
        frequance = {column: sum(df[column]) for column in df}
        print(frequance)



main_loop()