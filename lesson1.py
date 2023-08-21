import collections
import typing

UserData = collections.namedtuple("UserData", ["date", "task"])


def get_data() -> UserData:
    """Функция для получения данных от пользователя

    Args:

    Returns:
        UserData: Кортеж с данными, полученными от пользователя
    """
    date = input("Введите дату: ")
    task = input("Введите задачу: ")
    return UserData(date=date, task=task)


def task1() -> None:
    """Задание 1: Напишите программу, которая последовательно запрашивает у
    пользователя Дату и Описание задачи, а затем выводит их через пробел.

    Args:

    Returns:
        None: Функция отображает результаты через print и возвращает None
    """
    user_data = get_data()
    print(f"{user_data.date} {user_data.task}")


def task2() -> None:
    """Задание 2: Модифицируйте программу из задания 1 таким образом, чтобы
    запрос даты и задачи выполнялся трижды и после этого результаты
    выводились на экран построчно в формате: на одной строчке дата и
    задача через пробел.

    Args:

    Returns:
        None: Функция отображает результаты через print и возвращает None
    """

    results: typing.List[UserData] = []

    for _ in range(3):
        user_data = get_data()
        results.append(user_data)

    for record in results:
        print(f"{record.date} {record.task}")


def task3() -> typing.Dict[str, str]:
    """Задание 3: Модифицируйте программу из задания 2 таким образом, чтобы
    данные не выводились на экран, а сохранялись в словарь. Ключами в этом
    словаре должны быть даты, а значениями - соответствующие им задачи.

    Args:

    Returns:
        typing.Dict[str, str]: Словарь, кличи которого являются введенными
            датами, а значения - задачами на указанную дату
    """

    results: typing.Dict[str, str] = {}

    for _ in range(3):
        user_data = get_data()
        results[user_data.date] = user_data.task

    return results


if __name__ == "__main__":
    for index, task in enumerate([task1, task2, task3], start=1):
        print(f"Задача {index}:")
        results = task()
        if results:
            print(f"Результаты: {results}")
        print()
