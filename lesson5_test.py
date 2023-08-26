import dataclasses
import typing
import unittest
import unittest.mock
import uuid

import lesson5
import misc


@dataclasses.dataclass
class MessageWithOptionalAnswer:
    message: misc.TelegramBot.TelegramMessage
    is_answer: bool


class TestLesson5Task1(unittest.TestCase):
    def setUp(self) -> None:
        self.bot = misc.TelegramBot()

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("telebot.TeleBot", self.bot),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    def run_bot_requests(
        self,
        messages: typing.Iterable[str],
        tasks_file_name: typing.Optional[str] = None,
    ) -> typing.Tuple[misc.TelegramBot.SendedMessage, ...]:
        self.bot.messages_to_bot = [
            misc.TelegramBot.TelegramMessage(text=i) for i in messages
        ]
        self.bot.clear_messages_from_bot()

        lesson5.task1(token="", tasks_file_name=tasks_file_name)

        return self.bot.messages_from_bot

    def test_help_command(self) -> None:
        """Проверка ответов для команды /help"""
        # проверяем ответ на "/help"
        HELP = "\n".join(
            [
                "Список доступных команд:",
                "\t* show  - напечать все задачи на заданную дату",
                "\t* todo - добавить задачу",
                "\t* random - добавить на сегодня случайную задачу",
                "\t* help - Напечатать help",
            ]
        )

        answers = self.run_bot_requests(["/help"])

        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].text, HELP)

    def test_random(self) -> None:
        """Проверка ответов для команды /random"""
        # проверяем ответ на "/random"

        answers = self.run_bot_requests(["/random"])

        self.assertEqual(len(answers), 1)
        self.assertTrue(answers[0].text.startswith("Задача"))
        self.assertTrue(answers[0].text.endswith("добавлена на сегодня"))

    def test_add(self) -> None:
        """Проверка ответов для команды /add"""

        messages = [
            "/add сегодня тестовая задача",
            "/add сегодня A",
            "/add сегодня",
        ]

        answers = self.run_bot_requests(messages)

        self.assertEqual(len(answers), len(messages))
        self.assertEqual(
            answers[0].text,
            "Задача тестовая задача добавлена на дату сегодня",
        )
        self.assertEqual(
            answers[1].text,
            "Задача не может быть короче трех символов",
        )
        self.assertEqual(
            answers[2].text,
            "Команда составлена некорректно",
        )

    def test_show(self) -> None:
        """Проверка ответов для команды /show"""

        messages = [
            "/add сегодня тестовая задача",
            "/add завтра завтрашняя тестовая задача",
            "/add вчера тестовая задача @тестовая категория",
            "/show сегодня",
            "/show сегодня завтра",
            "/show такой_даты_нет",
            "/show",
            "/show вчера",
        ]
        answers = self.run_bot_requests(messages)

        self.assertEqual(len(answers), len(messages))

        self.assertEqual(
            answers[3].text.splitlines()[-1], "[ ] тестовая задача"
        )
        self.assertEqual(
            answers[4].text.splitlines(),
            [
                "[ ] тестовая задача",
                "[ ] завтрашняя тестовая задача",
            ],
        )

        self.assertEqual(answers[5].text.splitlines()[-1], "Такой даты нет")
        self.assertEqual(
            answers[6].text.splitlines()[-1],
            "Необходимо передать как минимум одну дату",
        )
        self.assertEqual(
            answers[7].text.splitlines()[-1],
            "[ ] тестовая задача @тестовая категория",
        )

    def test_store_tasks_in_file(self) -> None:
        """Проверка сохранения задач в файле"""

        # проверяем что если файл не указан таски между запусками
        # не сохраняются

        self.run_bot_requests(
            ["/add сегодня проверка сохранения заданий в файл"]
        )
        answers = self.run_bot_requests(["/show сегодня"])

        self.assertEqual(len(answers), 1)
        self.assertTrue(answers[0].text, "Такой даты нет")

        # проверяем что при указании файла задачи в него сохраняются
        tasks_file_name = f"/tmp/{uuid.uuid4().hex}.json"

        self.run_bot_requests(
            ["/add сегодня проверка сохранения заданий в файл"],
            tasks_file_name=tasks_file_name,
        )
        answers = self.run_bot_requests(
            ["/show сегодня"], tasks_file_name=tasks_file_name
        )

        self.assertEqual(len(answers), 1)
        self.assertTrue(
            answers[0].text, "[ ] проверка сохранения заданий в файл"
        )


if __name__ == "__main__":
    unittest.main()
