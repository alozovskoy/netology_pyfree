import random

import telebot


def task1(token: str) -> None:
    """orginal:
    https://github.com/netology-code/pyfree-homeworks/blob/main/code/todobot.py

    Расширьте функциональность бота возможностью на ваш выбор.
    Примеры дополнительных возможностей:

    Выводить ошибку при добавлении задачи, в которой меньше 3х символов.
    Печатать задачи на несколько дат: принимать в команде print не одну дату,
        а произвольное количество.
    При добавлении задачи учитывать отдельным параметром ее категорию. При
        выводе печатать категории задач со знаком @:
        "Помыть посуду @Домашние дела."
    """

    bot = telebot.TeleBot(token)

    RANDOM_TASKS = [
        "Написать Гвидо письмо",
        "Выучить Python",
        "Записаться на курс в Нетологию",
        "Посмотреть 4 сезон Рик и Морти",
    ]

    todos = dict()

    HELP = """
    Список доступных команд:
    * print  - напечать все задачи на заданную дату
    * todo - добавить задачу
    * random - добавить на сегодня случайную задачу
    * help - Напечатать help
    """

    def add_todo(date, task):
        date = date.lower()
        if todos.get(date) is not None:
            todos[date].append(task)
        else:
            todos[date] = [task]

    @bot.message_handler(commands=["help"])
    def help(message):
        bot.send_message(message.chat.id, HELP)

    @bot.message_handler(commands=["random"])
    def random_(message):
        task = random.choice(RANDOM_TASKS)
        add_todo("сегодня", task)
        bot.send_message(
            message.chat.id, f"Задача {task} добавлена на сегодня"
        )

    @bot.message_handler(commands=["add"])
    def add(message):
        _, date, tail = message.text.split(maxsplit=2)
        task = " ".join([tail])
        add_todo(date, task)
        bot.send_message(
            message.chat.id, f"Задача {task} добавлена на дату {date}"
        )

    @bot.message_handler(commands=["show"])
    def print_(message):
        date = message.text.split()[1].lower()
        if date in todos:
            tasks = ""
            for task in todos[date]:
                tasks += f"[ ] {task}\n"
        else:
            tasks = "Такой даты нет"
        bot.send_message(message.chat.id, tasks)

    bot.polling(none_stop=True)
