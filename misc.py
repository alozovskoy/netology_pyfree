import dataclasses
import io
import sys
import typing


class InputWrapper:
    """Обертка для input() - при каждом вызове возвращает строковое
    представление один из ранее переданных объектов (FIFO).
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
        self._data: typing.List[str] = []

        if data:
            self += data

    @property
    def data(self) -> typing.Tuple[str, ...]:
        """Данные, которые доступны на данный момент в экземпляре

        Args:

        Returns:
            typing.Tuple[str, ...]: Кортеж с данными
        """
        return tuple(self._data)

    def __iadd__(self, other: typing.Iterable[typing.Any]) -> "InputWrapper":
        """Расширяет список данных объекта элементами переданного перечисления.
        Объекты приводятся к строковому типу.

        Args:
            other (typing.Iterable[typing.Any]): Перечисляемый тип с данными,
                которые следует добавить к существующим данным объекта

        Returns:
            "InputWrapper": Экземпляр объекта с добавленными данными
        """
        self._data.extend(map(str, other))
        return self

    def clean(self) -> None:
        """Очистка списка данных экземпляра

        Args:

        Returns:
            None:
        """
        self._data = []

    def call(self, *args: typing.Any, **kwargs: typing.Any) -> str:
        """Вернуть один объект данных из доступных (FIFO)

        Args:
            args (typing.Any): Игнорируется
            kwargs (typing.Any): Игнорируется

        Returns:
            str: Объект данных, ранее переданных в экземпляр
        """
        assert args or kwargs or True
        try:
            return self._data.pop(0)
        except IndexError:
            raise ValueError("Не осталось данных")

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> str:
        """Вернуть один объект данных из доступных (FIFO)

        Args:
            args (typing.Any): Игнорируется
            kwargs (typing.Any): Игнорируется

        Returns:
            str: Объект данных, ранее переданных в экземпляр
        """
        assert args or kwargs or True
        return self.call()

    def __len__(self) -> int:
        """Возвращает количество имеющихся данных

        Args:

        Returns:
            int: Количество имеющихся данных
        """
        return len(self.data)


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

    def __len__(self) -> int:
        """Возвращает количество имеющихся данных

        Args:

        Returns:
            int: Количество имеющихся данных
        """
        return len(self.data)


class TelegramBot:
    @dataclasses.dataclass
    class TelegramChat:
        id: int = 0

    @dataclasses.dataclass
    class TelegramMessage:
        text: str
        content_type: str = "text"
        chat: "TelegramBot.TelegramChat" = dataclasses.field(
            default_factory=lambda: TelegramBot.TelegramChat()
        )

    @dataclasses.dataclass
    class SendedMessage:
        chat_id: int
        text: str

    def __init__(
        self, messages_to_bot: typing.Iterable[TelegramMessage]
    ) -> None:
        """Создание и наполнение необходимых структур

        Args:
            messages_to_bot (typing.List[TelegramMessage]): Список "сообщений",
                которые нужно "отправить" в бот

        Returns:
            None:
        """

        # Связь функций-обработчиков сообщений с content_type
        self._content_type_to_function_mappings: typing.Dict[
            str, typing.Callable[[TelegramBot.TelegramMessage], None]
        ] = {}
        self._command_to_function_mappings: typing.Dict[
            str, typing.Callable[[TelegramBot.TelegramMessage], None]
        ] = {}

        # Сообщения, которые нужно "отправить" боту
        self._messages_to_bot: typing.List[TelegramBot.TelegramMessage] = list(
            messages_to_bot
        )

        # Сообщения, которые "отправляет" бот в ответ
        self._messages_from_bot: typing.List[TelegramBot.SendedMessage] = []

    @property
    def messages_from_bot(
        self,
    ) -> typing.Tuple["TelegramBot.SendedMessage", ...]:
        return tuple(self._messages_from_bot)

    def __call__(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> "TelegramBot":
        """Иммитация инициализации - в качестве мока будет использоваться
        инстанс класса, который в коде будут пытаться "инициализировать"

        Args:
            args (typing.Any): Игнорируется
            kwargs (typing.Any): Игнорируется

        Returns:
            "TelegramBot": Инстанс мока бота
        """
        assert args or kwargs or True
        return self

    def message_handler(
        self,
        *args: typing.Any,
        content_types: typing.Optional[typing.List[str]] = None,
        commands: typing.Optional[typing.List[str]] = None,
        **kwargs: typing.Any
    ) -> typing.Callable[[typing.Callable[[TelegramMessage], None]], None]:
        """Декоратор для обработчика сообщений - сохраняет переданную функцию
        обработки сообщения со связанным content_type входящего сообщения

        Args:
            args: Игнорируется
            content_types (typing.Optional[typing.List[str]]): coontent_type'ы,
                к которым следует привязать декорируемую функцию
            commands (typing.Optional[typing.List[str]]): команды, к которым
                следует привязывать функцию
            kwargs: Игнорируется

        Returns:
            typing.Callable[[typing.Callable[[TelegramMessage], None]], None]:
                Враппер для функции обработчика сообщений с указанным
                content_type
        """
        assert args or kwargs or True

        if not content_types and not commands:
            raise ValueError(
                (
                    "Требуется передать или список команд ('commands'), или "
                    "список 'content_types', к которым следует привязывать "
                    "команды"
                )
            )

        if content_types is None:
            content_types = []

        if commands is None:
            commands = []

        def wrapper(
            function: typing.Callable[[TelegramBot.TelegramMessage], None]
        ) -> None:
            for content_type in content_types:
                self._content_type_to_function_mappings[
                    content_type
                ] = function

            for command in commands:
                self._command_to_function_mappings[command] = function

        return wrapper

    def send_message(self, chat_id: int, text: str) -> None:
        """Иммитация отправки сообщения - сообщение складывается в список
        отправленных сообщений инстанса

        Args:
            chat_id (int): ID чата в телеграм
            text (str): Текст сообщения

        Returns:
            None:
        """
        self._messages_from_bot.append(
            self.SendedMessage(chat_id=chat_id, text=text)
        )

    def polling(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """В библиотеке эта функция запускает бота - он подключается к серверу
        и начинает принимать и отправлять сообщения. В нашей иммитации
        сообщения из наполненного при инициализации списка передаются в
        функции, связанные с соответствующим content_type

        Args:
            args: Игнорируется
            kwargs: Игнорируется

        Returns:
            None:
        """
        assert args or kwargs or True
        for message in self._messages_to_bot:
            command = message.text.split(maxsplit=1)[0]

            if command.startswith("/"):
                function = self._command_to_function_mappings.get(
                    command.removeprefix("/")
                )
                if function:
                    function(message)
                    continue

            function = self._content_type_to_function_mappings.get(
                message.content_type
            )
            if function:
                function(message)
