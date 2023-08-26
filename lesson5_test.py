import dataclasses
import typing
import unittest
import unittest.mock

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
        self, messages: typing.Iterable[str]
    ) -> typing.Tuple[misc.TelegramBot.SendedMessage, ...]:
        self.bot.messages_to_bot = [
            misc.TelegramBot.TelegramMessage(text=i) for i in messages
        ]
        self.bot.clear_messages_from_bot()

        lesson5.task1(token="")

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

        answers = self.run_bot_requests(["/add сегодня тестовая задача"])

        self.assertEqual(len(answers), 1)
        self.assertEqual(
            answers[0].text,
            "Задача тестовая задача добавлена на дату сегодня",
        )

    def test_show(self) -> None:
        """Проверка ответов для команды /show"""

        answers = self.run_bot_requests(
            [
                "/add сегодня тестовая задача",
                "/show сегодня",
                "/show такой_даты_нет",
            ]
        )

        self.assertEqual(len(answers), 3)

        self.assertEqual(
            answers[1].text.splitlines()[-1], "[ ] тестовая задача"
        )

        self.assertEqual(answers[2].text.splitlines()[-1], "Такой даты нет")


if __name__ == "__main__":
    unittest.main()
