import typing


def original_function():
    HELP = """
    help - напечатать справку по программе.
    add - добавить задачу в список (название задачи запрашиваем у пользователя).
    show - напечатать все добавленные задачи."""

    tasks = []

    run = True

    while run:
        command = input("Введите команду: ")
        if command == "help":
            print(HELP)
        elif command == "show":
            print(tasks)
        elif command == "add":
            task = input("Введите название задачи: ")
            tasks.append(task)
            print("Задача добавлена")
        else:
            print("Неизвестная команда")
            break

    print("До свидания!")


def task1() -> None:
    """Модифицируйте программу, написанную на занятии так, чтобы выход из
    нее осуществлялся не только при вводе неизвестной команды, но и при вводе
    специальной команды exit. Сделайте так, чтобы при вводе этой команды
    программа выводила на экран текст: "Спасибо за использование!
    До свидания!"
    """

    HELP: typing.Final[str] = "\n".join(
        [
            "\thelp - напечатать справку по программе.",
            (
                "\tadd - добавить задачу в список (название задачи "
                "запрашиваем у пользователя)."
            ),
            "\tshow - напечатать все добавленные задачи.",
            "\texit - завершить работу программы",
        ]
    )

    tasks: typing.List[str] = []

    while True:
        command = input("Введите команду: ")
        if command == "help":
            print(HELP)
        elif command == "show":
            print(tasks)
        elif command == "add":
            task = input("Введите название задачи: ")
            tasks.append(task)
            print("Задача добавлена")
        elif command == "exit":
            print("Спасибо за использование! ", end="")
            break
        else:
            print("Неизвестная команда")
            break

    print("До свидания!")


def task2() -> None:
    """Сделайте следующие изменения:

    Заведите 3 списка: today, tomorrow, other (вы можете назвать переменные
    по-другому).
    Измените блок кода, который выполняет команду add:

    Дополнительно запросите у пользователя дату выполнения задачи.
    В зависимости от введенной даты добавьте задачу в один из списков по
    следующим правилам:
        Если пользователь ввел "Сегодня", добавьте задачу в список today.
        Если пользователь ввел "Завтра", добавьте задачу в список tomorrow.
        Если пользователь ввел любое другое значение, добавьте задачу в
            список other.
    """

    HELP: typing.Final[str] = "\n".join(
        [
            "\thelp - напечатать справку по программе.",
            (
                "\tadd - добавить задачу в список (название задачи и время "
                "ее выполнения запрашиваем у пользователя)."
            ),
            "\tshow - напечатать все добавленные задачи.",
            "\texit - завершить работу программы",
        ]
    )

    default_tasks_date: typing.Final[str] = "другое время"
    tasks: typing.Dict[str, typing.List[str]] = {
        "сегодня": [],
        "завтра": [],
        default_tasks_date: [],
    }

    while True:
        command = input("Введите команду: ")
        if command == "help":
            print(HELP)
        elif command == "show":
            for tasks_date, tasks_list in tasks.items():
                print(f'Задачи на {tasks_date}: {", ".join(tasks_list)}')
        elif command == "add":
            task = input("Введите название задачи: ")
            date = input("Введите дату выполнения задачи: ")

            tasks.get(date.lower(), tasks[default_tasks_date]).append(task)

            print("Задача добавлена")
        elif command == "exit":
            print("Спасибо за использование! ", end="")
            break
        else:
            print("Неизвестная команда")
            break

    print("До свидания!")


if __name__ == "__main__":
    print("======== Задание 1 ========")
    task1()
    print("======== Задание 2 ========")
    task2()
