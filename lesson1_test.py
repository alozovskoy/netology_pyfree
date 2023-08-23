import typing
import unittest
import unittest.mock

import lesson1
import misc


class TestLesson1(unittest.TestCase):
    def setUp(self) -> None:
        self.input_ = misc.InputWrapper()
        self.print_ = misc.PrintWrapper()

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("builtins.print", self.print_),
            unittest.mock.patch("builtins.input", self.input_),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_get_data(self) -> None:
        results = lesson1.UserData(date="ПН", task="Проверка функции get_data")

        self.input_.clean()
        self.input_ += [results.date, results.task]

        self.assertEqual(lesson1.get_data(), results)

    def test_task1(self) -> None:
        results = lesson1.UserData(date="ПН", task="Проверка функции task1")

        self.input_.clean()
        self.input_ += [results.date, results.task]

        lesson1.task1()

        self.assertEqual(
            self.print_.data[0], f"{results.date} {results.task}\n"
        )

    def test_task2(self) -> None:
        results = [
            lesson1.UserData(date="ПН", task="Проверка функции task2"),
            lesson1.UserData(date="ВТ", task="Вторая проверка функции task2"),
            lesson1.UserData(date="СР", task="Новая проверка функции task2"),
        ]

        self.input_.clean()
        for result in results:
            self.input_ += [result.date, result.task]

        self.print_.clean()

        lesson1.task2()

        for data_index, result in enumerate(results):
            self.assertEqual(
                self.print_.data[data_index], f"{result.date} {result.task}\n"
            )

    def test_task3(self) -> None:
        results = [
            lesson1.UserData(date="ЧТ", task="Проверка функции task3"),
            lesson1.UserData(date="ПТ", task="Вторая проверка функции task3"),
            lesson1.UserData(date="СБ", task="Новая проверка функции task3"),
        ]

        self.input_.clean()
        for result in results:
            self.input_ += [result.date, result.task]

        expected = {result.date: result.task for result in results}

        self.assertEqual(lesson1.task3(), expected)


if __name__ == "__main__":
    unittest.main()
