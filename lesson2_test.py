import typing
import unittest
import unittest.mock
import uuid

import lesson2
import misc


class TestLesson2Task1(unittest.TestCase):
    def setUp(self) -> None:
        self.input_ = misc.InputWrapper()
        self.print_ = misc.PrintWrapper()

        self._callable = lesson2.task1

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("builtins.print", self.print_),
            unittest.mock.patch("builtins.input", self.input_),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_exit(self) -> None:
        self.input_.clean()
        self.input_ += ["exit"]

        self.print_.clean()

        self._callable()

        expected_result = ("Спасибо за использование! ", "До свидания!\n")

        self.assertEqual(self.print_.data, expected_result)

    def test_unknown_command(self) -> None:
        self.input_.clean()
        self.input_ += [uuid.uuid4().hex]

        self.print_.clean()

        self._callable()

        expected_result = ("Неизвестная команда\n", "До свидания!\n")

        self.assertEqual(self.print_.data, expected_result)

    def test_help(self) -> None:
        self.input_.clean()
        self.input_ += ["help", "exit"]

        self.print_.clean()

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

        self._callable()

        self.assertEqual(len(self.print_), 3)
        self.assertEqual(self.print_.data[0], HELP + "\n")

    def test_add_and_show(self) -> None:
        self.input_.clean()
        self.input_ += ["show", "add", "Тестовая задача", "show", "exit"]

        self.print_.clean()

        self._callable()

        self.assertEqual(self.print_.data[0], "[]\n")  # show
        self.assertEqual(self.print_.data[1], "Задача добавлена\n")  # add
        self.assertEqual(self.print_.data[2], "['Тестовая задача']\n")  # show
        self.assertEqual(
            self.print_.data[3:],
            ("Спасибо за использование! ", "До свидания!\n"),
        )  # exit


class TestLesson2Task2(unittest.TestCase):
    def setUp(self) -> None:
        self.input_ = misc.InputWrapper()
        self.print_ = misc.PrintWrapper()

        self._callable = lesson2.task2

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("builtins.print", self.print_),
            unittest.mock.patch("builtins.input", self.input_),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_exit(self) -> None:
        self.input_.clean()
        self.input_ += ["exit"]

        self.print_.clean()

        self._callable()

        expected_result = ("Спасибо за использование! ", "До свидания!\n")

        self.assertEqual(self.print_.data, expected_result)

    def test_unknown_command(self) -> None:
        self.input_.clean()
        self.input_ += [uuid.uuid4().hex]

        self.print_.clean()

        self._callable()

        expected_result = ("Неизвестная команда\n", "До свидания!\n")

        self.assertEqual(self.print_.data, expected_result)

    def test_help(self) -> None:
        self.input_.clean()
        self.input_ += ["help", "exit"]

        self.print_.clean()

        HELP: typing.Final[str] = "\n".join(
            [
                "\thelp - напечатать справку по программе.",
                (
                    "\tadd - добавить задачу в список (название задачи и "
                    "время ее выполнения запрашиваем у пользователя)."
                ),
                "\tshow - напечатать все добавленные задачи.",
                "\texit - завершить работу программы",
            ]
        )

        self._callable()

        self.assertEqual(len(self.print_), 3)
        self.assertEqual(self.print_.data[0], HELP + "\n")

    def test_add_and_show(self) -> None:
        self.input_.clean()
        self.input_ += [
            "show",
            "add",
            "Задача на сегодня",
            "Сегодня",
            "add",
            "Задача на завтра",
            "завтра",
            "add",
            "Тест",
            "Тест",
            "add",
            "И еще одна задача на сегодня",
            "сегодня",
            "show",
            "exit",
        ]

        self.print_.clean()

        self._callable()

        # show
        self.assertEqual(
            self.print_.data[0:3],
            (
                "Задачи на сегодня: \n",
                "Задачи на завтра: \n",
                "Задачи на другое время: \n",
            ),
        )

        # add сегодня
        self.assertEqual(self.print_.data[3], "Задача добавлена\n")

        # add завтра
        self.assertEqual(self.print_.data[4], "Задача добавлена\n")

        # add в другое время
        self.assertEqual(self.print_.data[5], "Задача добавлена\n")

        # add "И еще одна задача на сегодня"
        self.assertEqual(self.print_.data[6], "Задача добавлена\n")

        # show
        self.assertEqual(
            self.print_.data[7:10],
            (
                (
                    "Задачи на сегодня: Задача на сегодня, "
                    "И еще одна задача на сегодня\n"
                ),
                "Задачи на завтра: Задача на завтра\n",
                "Задачи на другое время: Тест\n",
            ),
        )

        self.assertEqual(
            self.print_.data[-2:],
            ("Спасибо за использование! ", "До свидания!\n"),
        )


if __name__ == "__main__":
    unittest.main()
