import typing
import unittest
import unittest.mock

import lesson4
import misc


class TestLesson4Task1(unittest.TestCase):
    def setUp(self) -> None:
        username: typing.Final[str] = "Вася"

        self.messages: typing.Tuple[misc.TelegramBot.TelegramMessage, ...] = (
            misc.TelegramBot.TelegramMessage(text="/start"),
            misc.TelegramBot.TelegramMessage(text="test"),
            misc.TelegramBot.TelegramMessage(text="Проверка кириллицы"),
            misc.TelegramBot.TelegramMessage(text=f"Меня зовут {username}"),
        )

        self.bot = misc.TelegramBot(messages_to_bot=messages)

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("telebot.TeleBot", self.bot),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

        lesson4.task1(token="", username=username)

    def test_responses(self) -> None:
        # проверяем что были ответы на все сообщения
        self.assertEqual(len(self.bot.messages_from_bot), len(self.messages))

        # проверяем ответ на "/start"
        self.assertEqual(self.bot.messages_from_bot[0].text, "/start")

        # проверяем ответ на "test"
        self.assertEqual(self.bot.messages_from_bot[1].text, "test")

        # проверяем ответ на "Проверка кириллицы"
        self.assertEqual(
            self.bot.messages_from_bot[2].text, "Проверка кириллицы"
        )

        # проверяем ответ на строку с именем
        self.assertEqual(
            self.bot.messages_from_bot[3].text, "Ба! Знакомые все лица!"
        )


if __name__ == "__main__":
    unittest.main()
