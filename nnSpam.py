from asyncio import sleep
from .. import loader, utils

# Глобальная переменная для отслеживания активного спама
active_spam = {}

def register(cb):
    cb(NNSpamMod())

class NNSpamMod(loader.Module):
    """🌘 Модуль NNSpam ʕ￫ᴥ￩ʔ
    
    ℹ️ Модуль для спама текстом с опциональным тегом.

    Использование:
    .nnSpam <количество> [тег] <текст>
    .NnOff - остановить спам

    **Module BY @i_love_opeoo**
    """
    
    strings = {'name': 'NNSpam'}
    
    def __init__(self):
        self.name = self.strings['name']

    async def nnSpamcmd(self, message):
        """<количество> [тег] <текст> (реплай на сообщение пользователя)"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Кого спамить? Ответь на сообщение пользователя!</b>")
            return

        chat_id = message.chat_id  # Используем chat_id как ключ для отслеживания
        user_id = reply.sender_id
        args = utils.get_args_raw(message)

        if not args:
            count = None  # Если количество не указано, делаем бесконечный спам
            text = "Бесконечный спам!"  # Текст по умолчанию
        else:
            args = args.split(" ", 1)
            try:
                count = int(args[0]) if args[0].isdigit() else None
                text = args[1].strip() if len(args) > 1 else args[0].strip()
            except ValueError:
                await message.edit("<b>Некорректный формат. Используй: .nnSpam <количество> [тег] <текст></b>")
                return

        # Обработка тега
        if "|" in text:
            tag, text = text.split("|", 1)
            tag = tag.strip()
        else:
            tag = None

        # Формируем сообщение
        if tag:
            formatted_message = f"<a href=\"tg://user?id={user_id}\">{tag}</a>: {text.strip()}"
        else:
            formatted_message = f"<a href=\"tg://user?id={user_id}\">{text.strip()}</a>"

        # Запускаем спам
        active_spam[chat_id] = True
        await message.edit("<b>Начинаю спам!</b>")

        if count is None:
            # Бесконечный спам
            while active_spam.get(chat_id, False):
                await message.client.send_message(message.to_id, formatted_message)
                await sleep(0.3)
        else:
            # Ограниченный спам
            for _ in range(count):
                if not active_spam.get(chat_id, False):  # Проверка на остановку
                    break
                await message.client.send_message(message.to_id, formatted_message)
                await sleep(0.3)

        active_spam[chat_id] = False
        await message.edit("<b>Спам завершён!</b>")

    async def NnOffcmd(self, message):
        """Остановить спам"""
        chat_id = message.chat_id
        if active_spam.get(chat_id, False):
            active_spam[chat_id] = False
            await message.edit("<b>Спам остановлен!</b>")
        else:
            await message.edit("<b>Спам не активен!</b>")