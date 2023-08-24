import sys
import telebot


def original(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=["text"])
    def echo(message):
        bot.send_message(message.chat.id, message.text)

    bot.polling(none_stop=True)


def task1(token: str, username: str) -> None:
    '''Модифицируйте нашего ЭхоБота таким образом, чтобы в ответ на
    сообщение, в котором присутствует ваше имя, он не повторял его,
    а отвечал: "Ба! Знакомые все лица!"'''

    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=["text"])
    def echo(message):
        text = message.text

        if username.lower() in map(str.lower, text.split()):
            text = "Ба! Знакомые все лица!"

        bot.send_message(message.chat.id, text)

    bot.polling(none_stop=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <BOT_TOKEN> <USERNAME>")
    else:
        task1(token=sys.argv[1], username=sys.argv[2])
