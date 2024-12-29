from asyncio import sleep
from .. import loader, utils

# Глобальная переменная для отслеживания спама
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
        
        user_id = reply.sender_id
        args = utils.get_args_raw(message)
        
        if not args:
            await message.edit("<b>Не указано количество! Спамлю бесконечно...</b>")
            count = None  # Спам будет бесконечным
        else:
            args = args.split(" ", 1)
            try:
                count = int(args[0]) if args[0].isdigit() and int(args[0]) > 0 else 50
                if len(args) > 1:
                    text = args[1].strip()
                else:
                    await message.edit("<b>Укажи текст для спама!</b>")
                    return
            except ValueError:
                await message.edit("<b>Некорректный формат. Используй: .nnSpam <количество> [тег] <текст></b>")
                return
        
        if "|" in text:
            tag, text = text.split("|", 1)
            tag = tag.strip()
        else:
            tag = None
        
        if tag:
            formatted_message = f"<a href=\"tg://user?id={user_id}\">{tag}</a>: {text.strip()}"
        else:
            formatted_message = f"<a href=\"tg://user?id={user_id}\">{text.strip()}</a>"
        
        # Устанавливаем активный спам для данного пользователя
        active_spam[user_id] = True
        await message.edit("<b>Начинаю спам!</b>")

        # Бесконечный цикл или ограниченный, в зависимости от наличия count
        if count is None:
            while active_spam.get(user_id, False):
                await message.client.send_message(message.to_id, formatted_message)
                await sleep(0.3)
        else:
            for i in range(count):
                if not active_spam.get(user_id, False):
                    break
                await message.client.send_message(message.to_id, formatted_message)
                await sleep(0.3)

        # Завершаем спам
        await message.edit("<b>Спам завершён!</b>")
        active_spam[user_id] = False

    async def NnOffcmd(self, message):
        """Остановить спам"""
        user_id = message.sender_id
        if active_spam.get(user_id, False):
            active_spam[user_id] = False
            await message.edit("<b>Спам остановлен!</b>")
        else:
            await message.edit("<b>Спам не активен!</b>")