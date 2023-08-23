import typing


def count_letter(data: typing.Iterable[str], letter: str) -> int:
    """
    Реализуйте функцию count_letter, которая принимает список слов и
    некоторую букву и возвращает количество слов в списке, в которых эта
    буква встречается хотя бы один раз.

    Используйте конструкцию for word in ... для итерации по списку.
    Используйте переменную для хранения промежуточного результата подсчета.
    Используйте конструкцию letter in word для проверки наличия буквы в слове.
    """

    count: int = 0

    for word in data:
        if letter in word:
            count += 1

    return count
