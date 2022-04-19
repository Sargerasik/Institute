import csv
from math import floor

import pandas as pd


def stupid_hash(str):
    sum = 0
    for sym in str:
        sum += ord(sym)
    return sum


def read_file():
    """Чтение данных из таблицы. ФОрмирование таблицы транзакций."""
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

        frequance = {column: sum(df[column]) for column in df}  # Часто встречающийхся транкзакций.
        print(frequance)
        print(df)
        del_rare_categories(df, frequance)
        print(df)
        encode = {}
        create_hash_dict(encode, frequance)
        transition_table = create_transition(df, encode, frequance)
        F3 = []

        pair = list(map(set, encode.values()))
        pair_copy = pair.copy()
        print(pair)
        for pair1 in range(len(pair) - 1):
            for pair2 in range(pair1 + 1, len(pair)):

                if pair[pair1].intersection(pair[pair2]) != set():
                    pair_copy = pair[pair1].copy()
                    pair_copy.update(pair[pair2])
                    if pair_copy not in F3:
                        F3.append(pair_copy)
        print(F3)
        print(transition_table)


def create_hash_dict(encode, frequance):
    """Сотавление пар значений и их кодировки"""
    for key1 in frequance.keys():
        for key2 in frequance.keys():
            if key1 != key2:
                encode[stupid_hash(key1) + stupid_hash(key2)] = [key1, key2]


def del_rare_categories(df, frequance):
    """Удаление маловстречающийхся транкзакций. Порог - 70% от среднего числа"""
    porog = floor((sum(frequance.values()) / len(frequance.keys())) * 0.7)  # Порог
    items = list(frequance.items()).copy()
    for key, value in items:
        if value <= porog:
            del df[key]
            frequance.pop(key, None)
    del items


def create_transition(df, encode, frequance):
    """Составление таблицы транзакций пар"""
    transition_table = dict().fromkeys(encode.keys(), 0)
    porog = floor((sum(frequance.values()) / len(frequance.keys())) * 0.7)  # Порог
    keys = list(frequance.keys())
    for key1 in range(len(keys) - 1):
        for key2 in range(key1 + 1, len(keys)):
            for row in range(len(df.index)):
                if df[keys[key1]][row] == 1 and df[keys[key2]][row] == 1:
                    has_key = stupid_hash(keys[key1]) + stupid_hash(keys[key2])
                    transition_table[has_key] += 1

    return transition_table


read_file()
