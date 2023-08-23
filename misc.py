import io
import sys
import typing


class InputWrapper:
    """Обертка для input() - при каждом вызове возвращает один из ранее
    переданных объектов (FIFO).
    """

    def __init__(
        self, data: typing.Optional[typing.Iterable[typing.Any]] = None
    ) -> None:
        """Создание нового объекта

        Args:
            data (typing.Optional[typing.Iterable[typing.Any]]): Данные,
                которые стоит возвращает при вызове объекта

        Returns:
            None:
        """
        self._data: typing.List[typing.Any] = []

        if data:
            self += data

    @property
    def data(self) -> typing.Tuple[typing.Any, ...]:
        """Данные, которые доступны на данный момент в экземпляре

        Args:

        Returns:
            typing.Tuple[typing.Any, ...]: Кортеж с данными
        """
        return tuple(self._data)

    def __iadd__(self, other: typing.Iterable[typing.Any]) -> "InputWrapper":
        """Расширяет список данных объекта элементами переданного перечисления

        Args:
            other (typing.Iterable[typing.Any]): Перечисляемый тип с данными,
                которые следует добавить к существующим данным объекта

        Returns:
            "InputWrapper": Экземпляр объекта с добавленными данными
        """
        self._data.extend(other)
        return self

    def clean(self) -> None:
        """Очистка списка данных экземпляра

        Args:

        Returns:
            None:
        """
        self._data = []

    def call(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Вернуть один объект данных из доступных (FIFO)

        Args:
            args (typing.Any): Игнорируется
            kwargs (typing.Any): Игнорируется

        Returns:
            typing.Any: Объект данных, ранее переданных в экземпляр
        """
        assert args or kwargs or True
        try:
            return self._data.pop(0)
        except IndexError:
            raise ValueError("Не осталось данных")

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Вернуть один объект данных из доступных (FIFO)

        Args:
            args (typing.Any): Игнорируется
            kwargs (typing.Any): Игнорируется

        Returns:
            typing.Any: Объект данных, ранее переданных в экземпляр
        """
        assert args or kwargs or True
        return self.call()


class PrintWrapper:
    """Обертка для print() - вместо вывода данных в sys.stdout сохраняет их
    внутри экземпляра
    """

    _real_print = print

    def __init__(self) -> None:
        self._data: typing.List[str] = []

    @property
    def data(self) -> typing.Tuple[str, ...]:
        """Возвращает кортеж с хранящимися в экземпляре данными

        Args:

        Returns:
            typing.Tuple[str, ...]: Кортеж с хранящимися в экземпляре данными
        """
        return tuple(self._data)

    def clean(self) -> None:
        """Очистка списка хранящихся в экземпляре данных

        Args:

        Returns:
            None:
        """
        self._data = []

    def call(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Сохранить данные в экземпляре

        Args:
            args (typing.Any): Аргументы аналогичные print()
            kwargs (typing.Any): KW-аргументы аналогичные print()

        Returns:
            None:
        """
        buffer = io.StringIO()
        sys.stdout = buffer

        self._real_print(*args, **kwargs)

        print_output = buffer.getvalue()
        sys.stdout = sys.__stdout__

        self._data.append(print_output)

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Сохранить данные в экземпляре

        Args:
            args (typing.Any): Аргументы аналогичные print()
            kwargs (typing.Any): KW-аргументы аналогичные print()

        Returns:
            None:
        """
        return self.call(*args, **kwargs)
