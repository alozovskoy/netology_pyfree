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


class TestPrint(unittest.TestCase):
    """Тестирование wrapper'а для print()"""

    def setUp(self) -> None:
        self.print_ = misc.PrintWrapper()

        self.patches: typing.List[unittest.mock._patch] = [  # type: ignore
            unittest.mock.patch("builtins.print", self.print_),
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
        raw_result = "foobar"
        expected_result = f"{raw_result}\n"

        self.print_.clean()

        print(raw_result)

        self.assertEqual(len(self.print_.data), 1)
        self.assertEqual(self.print_.data[0], expected_result)

    def test_multiple(self) -> None:
        """Тестирование нескольких вызовов

        Args:

        Returns:
            None:
        """
        raw_results = ("foo", "bar")
        expected_results = tuple(f"{i}\n" for i in raw_results)

        self.print_.clean()

        for i in raw_results:
            print(i)

        self.assertEqual(len(self.print_.data), 2)
        self.assertEqual(self.print_.data, expected_results)

    def test_sep(self) -> None:
        """Тестирование разделителей

        Args:

        Returns:
            None:
        """
        raw_results = ("foo", "bar")

        expected_results = (
            " ".join(raw_results) + "\n",
            "-".join(raw_results) + "\n",
            "\t".join(raw_results) + "\n",
        )

        self.print_.clean()

        print(*raw_results)
        print(*raw_results, sep="-")
        print(*raw_results, sep="\t")

        self.assertEqual(self.print_.data, expected_results)

    def test_end(self, end: typing.Optional[str] = None) -> None:
        """Тестирование окончаний строк

        Args:

        Returns:
            None:
        """

        raw_result = "foobar"

        raw_ends = (None, "", " ", "\t")
        exp_ends = ("\n", "", " ", "\t")

        expected_results = tuple(f"{raw_result}{end}" for end in exp_ends)

        self.print_.clean()

        for end in raw_ends:
            print(raw_result, end=end)

        self.assertEqual(self.print_.data, expected_results)


if __name__ == "__main__":
    unittest.main()
