import dataclasses
import textwrap
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
        self.messages: typing.Tuple[MessageWithOptionalAnswer, ...] = (
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(text="/start"),
                is_answer=False,
            ),
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(text="/help"),
                is_answer=True,
            ),
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(text="/random"),
                is_answer=True,
            ),
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(
                    text="/add сегодня тестовая задача"
                ),
                is_answer=True,
            ),
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(text="/show сегодня"),
                is_answer=True,
            ),
            MessageWithOptionalAnswer(
                message=misc.TelegramBot.TelegramMessage(text="/show завтра"),
                is_answer=True,
            ),
        )

        self.bot = misc.TelegramBot(
            messages_to_bot=[i.message for i in self.messages]
        )

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("telebot.TeleBot", self.bot),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

        lesson5.task1(token="")

    def test_responses_count(self) -> None:
        """Проверяем что были ответы на все сообщения, на которые ожидался \
ответ"""
        self.assertEqual(
            len(self.bot.messages_from_bot),
            len(list(filter(lambda x: x.is_answer, self.messages))),
        )

    def test_help_command(self) -> None:
        """Проверка ответов для команды /help"""
        # проверяем ответ на "/help"
        HELP = "\n".join(
            [
                "Список доступных команд:",
                "\t* print  - напечать все задачи на заданную дату",
                "\t* todo - добавить задачу",
                "\t* random - добавить на сегодня случайную задачу",
                "\t* help - Напечатать help",
            ]
        )
        self.assertEqual(self.bot.messages_from_bot[0].text, HELP)

    def test_random(self) -> None:
        """Проверка ответов для команды /random"""
        # проверяем ответ на "/random"

        self.assertTrue(
            self.bot.messages_from_bot[1].text.startswith("Задача")
        )
        self.assertTrue(
            self.bot.messages_from_bot[1].text.endswith("добавлена на сегодня")
        )

    def test_add(self) -> None:
        """Проверка ответов для команды /add"""
        # проверяем ответ на "/add сегодня тестовая задача"
        self.assertEqual(
            self.bot.messages_from_bot[2].text,
            "Задача тестовая задача добавлена на дату сегодня",
        )

    def test_show(self) -> None:
        """Проверка ответов для команды /show"""

        # проверяем ответ на "/show сегодня"
        # первой записью будет рандомная задача из теста /random

        self.assertTrue(
            len(self.bot.messages_from_bot[3].text.splitlines()),
            2,
        )

        self.assertEqual(
            self.bot.messages_from_bot[3].text.splitlines()[-1],
            "[ ] тестовая задача",
        )

        # проверяем ответ на "/show завтра"
        self.assertTrue(
            len(self.bot.messages_from_bot[3].text.splitlines()),
            1,
        )
        self.assertEqual(
            self.bot.messages_from_bot[4].text.splitlines()[0],
            "Такой даты нет",
        )


if __name__ == "__main__":
    unittest.main()
