# Задание 1. Встроенные типы данных, операторы, функции и генераторы
#
# Напишите реализации объявленных ниже функций. Для проверки
# корректности реализации ваших функций, запустите тесты:
#
# pytest test_homework01.py
#
# Если написанный вами код не содержит синтаксических ошибок,
# вы увидите результаты тестов ваших решений.


def fac(n):
    """
    Факториал

    Факториал числа N - произведение всех целых чисел от 1 до N
    включительно. Например, факториал числа 5 - произведение
    чисел 1, 2, 3, 4, 5.

    Функция должна вернуть факториал аргумента, числа n.
    """
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def gcd(a, b):
    """
    Наибольший общий делитель (НОД) для двух целых чисел.

    Предполагаем, что оба аргумента - положительные числа
    Один из самых простых способов вычесления НОД - метод Эвклида,
    согласно которому

    1. НОД(a, 0) = a
    2. НОД(a, b) = НОД(b, a mod b)

    (mod - операция взятия остатка от деления, в python - оператор '%')
    """
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a

    return a + b


def fib():
    """
    Генератор для ряда Фибоначчи

    Вам необходимо сгенерировать бесконечный ряд чисел Фибоначчи,
    в котором каждый последующий элемент ряда является суммой двух
    предыдущих. Начало последовательности: 1, 1, 2, 3, 5, 8, 13, ..

    Подсказка по реализации: для бесконечного цикла используйте идиому

    while True:
      ..

    """
    x1, x2 = 0, 1
    yield 1

    while True:
        x1 = x1 + x2
        yield x1
        x2 = x1 + x2
        yield x2


def flatten(seq):
    """
    Функция, преобразующая вложенные последовательности любого уровня
    вложенности в плоские, одноуровневые.

    >>> flatten([])
    []
    >>> flatten([1, 2])
    [1, 2]
    >>> flatten([1, [2, [3]]])
    [1, 2, 3]
    >>> flatten([(1, 2), (3, 4)])
    [1, 2, 3, 4]
    """
    lst = list()

    for x in seq:
        if type(x) == list or type(x) == tuple:
            lst += flatten(x)
        else:
            lst.append(x)

    return lst
