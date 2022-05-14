import csv
from math import floor

import pandas as pd


def stupid_hash(str):
    sum = 0
    for sym in str:
        sum += ord(sym)
    return sum


def create_rule_v2(pairs, df):
    pairs = list(map(list, pairs))
    temp = []
    for pair in pairs:
        temp.append(pair.copy())
        pair.reverse()
        temp.append(pair)
    print(temp)
    sup_table = []
    for pair in temp:
        supp, auth = check_support(pair, df=df)
        if supp > 15 and auth > 50:
            sup_table.append((pair, supp, auth))
    print(sup_table)
    return sup_table


def create_association_table(rule, df):
    association_table = []
    rule = list(map(list, rule))
    for r in rule:
        for i in r:
            supp, auth = check_support(list(i), df)
            if supp > 15 and auth > 50:
                association_table.append((i, supp, auth))
    return association_table


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
        porog = floor((sum(frequance.values()) / len(frequance.keys())) * 0.7)  # Порог
        del_rare_categories(df, frequance, porog)
        print(df)
        encode = create_hash_dict(frequance)
        pair = list(map(tuple, encode.values()))
        transition_table_v2 = create_transition_v2(pair, df, porog)
        frequent_pair = list(transition_table_v2.keys())
        transition_table_v3 = create_transition_table_v3(frequent_pair)
        rule = [dependence(transition_table_v3[i], df) for i in range(len(transition_table_v3))]
        association_table = create_association_table(rule, df)
        association_table += create_rule_v2(frequent_pair, df)
        for p in association_table:
            print(f'rule: {p[0]} support: {p[1]} auth: {p[2]}')


def check_support(roule, df):
    """
    Проверка поддержки и достоверность одного правила. правило интерпретируется как [a, b] = Если a ТО b
    [a,b,c] = Если a и b То с
    :param roule:
    :param df:
    :return:
    """
    support = 0
    component = 0
    for row in range(len(df.index)):
        flag = True
        for j in range(len(roule) - 1):
            flag *= df[roule[j]][row] == 1
        if flag:
            component += 1
            if df[roule[-1]][row] == 1:
                support += 1
    return support / len(df.index) * 100, support / component * 100


def dependence(s: tuple, df):
    ss = []
    for i in range(len(s) - 1):
        for j in range(i + 1, len(s)):
            ss.append(tuple([s[i], s[j]]))
    print(s)
    print(ss)
    roule = set()
    for i in ss:
        for j in s:
            if j not in i:
                t = list(i)
                t.append(j)
                roule.add(tuple(t))
    return roule


def create_transition_table_v3(pair):
    F3 = []
    pair = list(map(set, pair))
    for pair1 in range(len(pair) - 1):
        for pair2 in range(pair1 + 1, len(pair)):
            if pair[pair1].intersection(pair[pair2]) != set():
                pair_copy = pair[pair1].copy()
                pair_copy.update(pair[pair2])
                if pair_copy not in F3:
                    F3.append(pair_copy)
    return list(map(tuple, F3))


def create_transition_v2(pair, df, porog):
    """
    Составление таблицы транзакций пар.
    удаление нечастых пар.
    """
    transition_table = dict()
    for p in pair:
        print(p)
        for row in range(len(df.index)):
            if df[p[0]][row] == 1 and df[p[1]][row]:
                if transition_table.get(p, None) is None:
                    transition_table[p] = 1
                else:
                    transition_table[p] += 1
    for key, value in transition_table.copy().items():
        if value < porog:
            transition_table.pop(key)
    return transition_table


def create_hash_dict(frequance):
    """Сотавление пар значений и их кодировки"""
    encode = {}
    for key1 in frequance.keys():
        for key2 in frequance.keys():
            if key1 != key2:
                encode[stupid_hash(key1) + stupid_hash(key2)] = [key1, key2]
    return encode


def del_rare_categories(df, frequance, porog):
    """Удаление маловстречающийхся транкзакций. Порог - 70% от среднего числа"""
    items = list(frequance.items()).copy()
    for key, value in items:
        if value <= porog:
            del df[key]
            frequance.pop(key, None)
    del items

if __name__ == '__main__':
    read_file()
