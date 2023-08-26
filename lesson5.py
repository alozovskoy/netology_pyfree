import dataclasses
import json
import random
import sys
import typing

import telebot


def task1(token: str, tasks_file_name: typing.Optional[str] = None) -> None:
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

    @dataclasses.dataclass
    class TodoTask:
        task: str
        category: typing.Optional[str] = None

    class TodoTaskJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    class TodoTaskJSONDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(
                self, object_hook=self.object_hook, *args, **kwargs
            )

        def object_hook(self, dct):
            if set(dct.keys()) == {"task", "category"}:
                return TodoTask(**dct)

            return dct

    todos: typing.Dict[str, typing.List[TodoTask]] = dict()

    if tasks_file_name:
        try:
            with open(tasks_file_name, "r") as tasks_file:
                json_data = json.load(tasks_file, cls=TodoTaskJSONDecoder)
                todos = json_data
        except FileNotFoundError:
            pass

    HELP = "\n".join(
        [
            "Список доступных команд:",
            (
                "\t* show <дата> [<дата>, ...] - "
                "напечать все задачи на заданную дату"
            ),
            "\t* add <дата> <задача> [@категория] - добавить задачу",
            "\t* random - добавить на сегодня случайную задачу",
            "\t* help - Напечатать help",
        ]
    )

    def add_todo(
        date: str, task: str, category: typing.Optional[str] = None
    ) -> None:
        """Добавить задачу в список дел

        Args:
            date (str): Дата, когда необходимо выполнять задачу
            task (str): Задача
            category (typing.Optional[str]): Категория

        Returns:
            None:
        """

        date = date.lower()

        if date not in todos:
            todos[date] = []

        todos[date].append(TodoTask(task=task, category=category))

        if tasks_file_name:
            with open(tasks_file_name, "w") as tasks_file:
                json.dump(todos, tasks_file, cls=TodoTaskJSONEncoder)

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
        try:
            _, date, task = message.text.split(maxsplit=2)
        except ValueError:
            bot.send_message(message.chat.id, "Команда составлена некорректно")
            return

        if len(task) < 3:
            bot.send_message(
                message.chat.id, "Задача не может быть короче трех символов"
            )
            return

        if " @" in task:
            try:
                task, category = task.split(" @")
            except ValueError:
                category = None
        else:
            category = None

        add_todo(date, task, category)
        bot.send_message(
            message.chat.id, f"Задача {task} добавлена на дату {date}"
        )

    @bot.message_handler(commands=["show"])
    def show(message):
        dates = list(map(str.lower, message.text.split()[1:]))

        if not dates:
            bot.send_message(
                message.chat.id, "Необходимо передать как минимум одну дату"
            )
            return
        tasks = []

        for date in dates:
            if date in todos:
                for task in todos[date]:
                    _task = f"[ ] {task.task}"
                    if task.category:
                        _task += f" @{task.category}"
                    tasks.append(_task)

        if tasks:
            tasks = "\n".join(tasks)
        else:
            tasks = "Такой даты нет"

        bot.send_message(message.chat.id, tasks)

    bot.polling(none_stop=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <BOT_TOKEN>")
    else:
        task1(token=sys.argv[1])
