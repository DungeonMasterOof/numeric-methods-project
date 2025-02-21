# Программа написана на языке Python и выводит результаты в 2 таблицах в командной строке
# и в файлы в формате .csv: data1.csv - первый интеграл,
# data2.csv - второй.


import math as m
import pandas as pd
import numpy as np


def polinomQ(x):  # Полином Q(x)
    s = 0
    for i in range(0, 10):
        s += (m.comb(9, i))**2 * (x+1)**i * (x-1)**(9-i)

    s *= m.factorial(9)
    return s


def polinomP(x):  # Полином P2(x)
    return 64 * x ** 6 - 80 * x ** 4 + 24 * x * x - 1


def bothPQ(x):  # Произведение полиномов Q(x) * P2(x)
    return polinomQ(x) * polinomP(x)


def rectangle_method(func, left_border, right_border, n):
    # Метод прямоугольника для разбиения на n отрезков
    res = 0.0
    step = (right_border - left_border) / n
    for x in np.arange(left_border, right_border, step):
        res += step * func(x + step)
    return res


def gauss_method(func):  # Метод Гаусса для n = 3
    res = 0.0
    values = [-m.sqrt(0.6), 0, m.sqrt(0.6)]  # Список корней полинома Лежандра
    weights = [5.0 / 9, 8.0 / 9, 5.0 / 9]  # Список весов
    num = len(values)
    for i in range(num):
        res += weights[i] * func(values[i])
    return res


# Инициализируем таблицу в pandas для фиксации в дальнейшем результатов
data1 = pd.DataFrame([[11, -1.0, -1.0, -1.0],
                      [21, -1.0, -1.0, -1.0],
                      [41, -1.0, -1.0, -1.0],
                      [81, -1.0, -1.0, -1.0],
                      [161, -1.0, -1.0, -1.0]],
columns=['Число узлов', 'Метод правых прямоугольников', 'Сходимость',
         'Метод Гаусса'])

data2 = data1.copy(deep=True)
nlist = [11, 21, 41, 81, 161]  # Список количеств узлов. n узлов => n-1 отрезок

# Таблица 1 (первый интеграл)
gauss = gauss_method(polinomQ)  # Достаточно вычислить 1 раз
for i in range(len(nlist)):
    data1.loc[i, "Метод правых прямоугольников"] = rectangle_method(polinomQ,
                -1, 1, nlist[i] - 1)
    temp = data1.loc[i, "Метод правых прямоугольников"]
    data1.loc[i, "Сходимость"] = m.log2(abs(temp / rectangle_method(polinomQ,
                -1, 1, 2 * (nlist[i] - 1))))
    data1.loc[i, "Метод Гаусса"] = gauss

# Таблица 2 (второй интеграл)
gauss = gauss_method(bothPQ)
for i in range(len(nlist)):
    data2.loc[i, "Метод правых прямоугольников"] = rectangle_method(bothPQ,
                -1, 1, nlist[i] - 1)
    temp = data2.loc[i, "Метод правых прямоугольников"]
    data2.loc[i, "Сходимость"] = m.log2(abs(temp / rectangle_method(bothPQ,
                -1, 1, 2 * (nlist[i] - 1))))
    data2.loc[i, "Метод Гаусса"] = gauss

# Вывод таблиц в командную строку
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(data1)
    print("\n\n\n")
    print(data2)

# Вывод в файлы формата .csvДля
data1.to_csv("data1.csv")
data2.to_csv("data2.csv")
