import typing
import unittest
import unittest.mock

import misc


class TestInput(unittest.TestCase):
    """Тестирование wrapper'а для input()"""

    def setUp(self) -> None:
        self.input_ = misc.InputWrapper()

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("builtins.input", self.input_),
        ]

        for patch in self.patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_simple(self) -> None:
        """Тестирование простого вызова

        Args:

        Returns:
            None:
        """
        expected_result = "foobar"

        self.input_.clean()
        self.input_ += [expected_result]

        data = input()

        self.assertEqual(data, expected_result)

    def test_multiple(self) -> None:
        """Тестирование нескольких вызовов - проверка как работает переданный
        список данных

        Args:

        Returns:
            None:
        """
        expected_result = ("foo", "bar")

        self.input_.clean()
        self.input_ += expected_result

        data1 = input()
        data2 = input()

        self.assertEqual((data1, data2), expected_result)

    def test_type_cast(self) -> None:
        """Тестирование преобразования типов - input должен возвращать строки
        вне зависимости от того, какие данны были положены во wrapper

        Args:

        Returns:
            None:
        """
        raw_values = (
            "str",
            1,
            0x2,
            ["l", "i", "s", "t"],
            ("t", "u", "p", "l", "e"),
            {"set is unordered, so thre is one value"},
            "строка с кириллицей",
        )

        expected_result = tuple(map(str, raw_values))

        self.input_.clean()
        self.input_ += raw_values

        data = []

        for _ in range(len(raw_values)):
            data.append(input())

        data = tuple(data)

        self.assertEqual(data, expected_result)
        self.assertTrue(all(isinstance(i, str) for i in data))

    def test_with_prompt(self) -> None:
        """Проверка работы с переданной срокой с подсказкой

        Args:

        Returns:
            None:
        """
        expected_result = "foobar"

        self.input_.clean()
        self.input_ += [expected_result]

        data = input("Эта строка не должна отобразиться")

        self.assertEqual(data, expected_result)


if __name__ == "__main__":
    unittest.main()
