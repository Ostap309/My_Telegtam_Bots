import functools

from telegram import ForceReply, Update
from telegram.ext import ContextTypes, ConversationHandler

DEBUG_MODE = True


def debug_print_return_code(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)  # вызываем функцию и сохраняем результат
        if DEBUG_MODE:
            print(f"DEBUG |  {func.__name__} -> CODE {result}")
        return result  # обязательно возвращаем результат!

    return wrapper


# Команда запуска телеграмм-бота
@debug_print_return_code
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат: /start

    chat = update.effective_chat
    chat_type = update.effective_chat.type

    if chat_type == "private":
        await update.message.reply_html(
            rf"Моё время пришло. Я рад приветствовать тебя, {update.effective_user.mention_html()}!"
        )
    elif chat_type in ["group", "supergroup", "channel"]:
        await update.message.reply_text(
            rf"Моё время пришло. Я рад приветствовать участников сообщества {chat.title}!"
        )
    else:
        await update.message.reply_text(
            rf"ГДЕ ЭТО Я, ЧЁРТ ПОБЕРИ!"
        )

    return 0


# Команда вызова документации
@debug_print_return_code
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат: /help

    await update.message.reply_text("Не могу ничем помочь, мой разработчик пока забил на эту функцию")

    return 0


# Команда добавления новой Выборки
@debug_print_return_code
async def add_selection_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат: /add_selection <selection_name: String>

    args = update.message.text.split()[1:]
    if not args:
        await update.message.reply_text(f"Прошу, повторите команду, указав имя новой Выборки.")
        return 400
    selection_name = " ".join(args)
    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.add_selection(selection_name)
    if storekeeper_code == 409:
        await update.message.reply_text(f"Выборка «{selection_name}» уже существует.")
    elif storekeeper_code == 0:
        await update.message.reply_text(f"Выборка «{selection_name}» успешно добавлена!")

    return storekeeper_code


@debug_print_return_code
async def get_all_selections_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /get_all_selections

    storekeeper = context.bot_data['storekeeper']
    output = "\n".join(map(lambda i: f"🔸 «{i}»", storekeeper.get_all_selections()))

    await update.message.reply_text(f"Вот список всех Выборок, которые можно использовать:\n{output}")

    return 0


@debug_print_return_code
async def undo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /undo

    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.undo()

    if storekeeper_code == 0:
        await update.message.reply_text(f"Все изменения текущей сессии отменены.")

    return storekeeper_code


@debug_print_return_code
async def save_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /save

    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.save()

    if storekeeper_code == 0:
        await update.message.reply_text(f"Все изменения текущей сессии сохранены.")

    return storekeeper_code

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)
