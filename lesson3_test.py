import unittest

import lesson3


class TestLesson3(unittest.TestCase):
    def setUp(self) -> None:
        self.data = ["python", "c++", "c", "scala", "java"]

    def test_c(self) -> None:
        letter = "c"
        expected = 3

        self.assertEqual(lesson3.count_letter(self.data, letter), expected)

    def test_a(self) -> None:
        letter = "a"
        expected = 2

        self.assertEqual(lesson3.count_letter(self.data, letter), expected)

    def test_q(self) -> None:
        letter = "q"
        expected = 0

        self.assertEqual(lesson3.count_letter(self.data, letter), expected)

    def test_cyrillic(self) -> None:
        letter = "Й"
        expected = 0

        self.assertEqual(lesson3.count_letter(self.data, letter), expected)

    def test_raises(self) -> None:
        with self.assertRaises(TypeError):
            for incorrect_object in (1, ["list"], ("tuple",), {"set"}):
                lesson3.count_letter(
                    self.data,
                    incorrect_object,  # type: ignore
                )


if __name__ == "__main__":
    unittest.main()
