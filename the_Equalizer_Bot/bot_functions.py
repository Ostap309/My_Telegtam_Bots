import functools

from telegram import Update
from telegram.ext import ContextTypes

# Режим вывода кодов возврата в консоль
DEBUG_MODE = True


# Функция-декоратор вывода кодов возврата в консоль (при DEBUG_MODE = True)
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

    await update.message.reply_text(
        """Этот бот предназначен для проведения честных голосований в рамках группового чата. Он позволяет случайным образом бесповторно выбирать предложенные пользователями варианты ответа, при этом обеспечивая очередность участников, что позволяет равномерно озвучивать идеи от каждого члена группы.
        
🔤 Терминология:
В рамках некоторого обсуждения пользователи могут создать Выборку(📋), которая будет являться хранилищем для всех Идей(💡), предложенных участниками этой дискуссии. Пользователь может создавать из своих Идей(💡) Очереди(⏳), если он хочет чтобы они выдвигались на всеобщее обозрение в определенном порядке (например фильмы во франшизе лучше смотреть по порядку)."""
    )

    await update.message.reply_text(
        """🛠️ Команды:

[🚀]
/start (или /st) - отображение приветствия

[❓]
/help (или /h) - небольшая документация по боту

[➕👤]
/add_me (или /am) - добавляет вас в мой активный список пользователей

[➕📋]
/add_selection (или /adds) <имя Выборки(📋)> - добавляет новую Выборку(📋) и делает её текущей

[🗂️]
/get_all_selections (или /gas) - выводит имена всех Выборок(📋), отображая текущую со знаком ✅

[💾]
/save (или /sv) - сохраняет все изменения текущей сессии работы моего сервера

[❌]
/undo (или /u) - откатывает все изменения текущей сессии работы моего сервера к предыдущему сохранению

[✅]
/current (или /cur) - выводит название текущей Выборки(📋)

[📌]
/set_current (или /sc) <имя Выборки(📋)> - выбирает новую текущую Выборку(📋) по вашему усмотрению

[✨]
/get_all_proposals (или /gap) - Выводит имена участников и их Идеи(💡) в текущей Выборке(📋)

[➕💡]
/add_proposals (или /addp) <номер Очереди(⏳)>; <Идея(💡)>; <Идея(💡)>; ...; <Идея(💡)> - добавляет одну или несколько Идей(💡) в текущую Выборку(📋) с назначением Очереди(⏳) (номер равный 0 добавляет элемент без Очереди(⏳))

[🔀]
/shuffle_order (или /shf) - перемешивает порядок пользователей в голосовании

[🎲]
/choose (или /ch) - выбирает Идею(💡), исключая её из Выборки(📋)"""
    )

    return 0


# Команда добавления новой Выборки
@debug_print_return_code
async def add_selection_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат: /add_selection <selection_name: String>

    args = update.message.text.split()[1:]
    if not args:
        await update.message.reply_text("Прошу, повторите команду, указав имя новой Выборки.")
        return 400
    selection_name = " ".join(args)
    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.add_selection(selection_name)

    if storekeeper_code == 409:
        await update.message.reply_text(f"Выборка «{selection_name}» уже существует.")

    elif storekeeper_code == 0:
        selection = context.bot_data['selection']
        selection.refresh()
        await update.message.reply_text(f"Выборка «{selection_name}» успешно добавлена!")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code


# Команда вывода всех существующих Выборок
@debug_print_return_code
async def get_all_selections_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /get_all_selections

    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.get_all_selections()

    if storekeeper_code == 0:
        output = "\n".join(map(
            lambda i: f"🔸 «{i}»" if i != storekeeper.current_selection else f"🔸 «{i}» ✅",
            storekeeper.all_selections_list))
        await update.message.reply_text(f"Вот список всех Выборок, которые можно использовать:\n{output}")

    elif storekeeper_code == 200:
        await update.message.reply_text(f"Ой, похоже список Выборок пуст.")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code


# Команда отмены всех несохраненных действий
@debug_print_return_code
async def undo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /undo

    storekeeper = context.bot_data['storekeeper']
    selection = context.bot_data['selection']

    storekeeper_code = storekeeper.undo()

    if storekeeper_code == 0:
        selection.refresh()
        await update.message.reply_text("Все изменения текущей сессии отменены.")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code


# Команда сохранения всех примененных действий в файл data.xlsx
@debug_print_return_code
async def save_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /save

    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.save()

    if storekeeper_code == 0:
        await update.message.reply_text("Все изменения текущей сессии сохранены.")

    elif storekeeper_code == 403:
        await update.message.reply_text(
            "Похоже моя база данных уже используется другим устройством, повторите попытку позже."
        )

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code


# Команда вывода текущей Выборки
@debug_print_return_code
async def current_selection_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /current

    storekeeper = context.bot_data['storekeeper']

    selection_code = storekeeper.get_current_selection_code()

    if selection_code == 0:
        await update.message.reply_text(f"Текущая Выборка: «{storekeeper.current_selection}»")

    elif selection_code == 200:
        await update.message.reply_text("В данный момент Выборок нет, но вы всегда можете добавить новую")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return selection_code


# Команда перехода на другую Выборку (делает указанную Выборку текущей)
@debug_print_return_code
async def set_current_selection_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /set_current <selection_name: String>

    args = update.message.text.split()[1:]
    if not args:
        await update.message.reply_text("Прошу, повторите команду, указав имя Выборки.")
        return 400
    selection_name = " ".join(args)
    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.set_current_selection(selection_name)

    if storekeeper_code == 404:
        await update.message.reply_text("Такой выборки не существует")

    elif storekeeper_code == 0:
        selection = context.bot_data['selection']
        selection.refresh()

        await update.message.reply_text(f"Успех! Текущая выборка: «{storekeeper.current_selection}»")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code


# Команда вывода всех Идей в текущей Выборке
@debug_print_return_code
async def get_all_proposals_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /get_all_proposals

    selection = context.bot_data['selection']

    selection_code = selection.show_proposals()

    if selection_code == 0:
        await update.message.reply_html(selection.answer_string)

    elif selection_code == 200:
        await update.message.reply_text(
            "Похоже текущая Выборка пустует:(\nНо вы можете стать первым, кто озвучит свою Идею!"
        )

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return selection_code


# Команда добавления Идей в текущую Выборку
@debug_print_return_code
async def add_proposals_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /add_proposals
    # <group_number: Integer>; <proposal_1: String>; <proposal_2: String>; ...; <proposal_n: String>

    args = update.message.text.split(" ")[1:]
    if not args:
        await update.message.reply_text(
            "Прошу, повторите команду, указав номер очереди (0 - без очереди), а затем свои Идеи."
        )
        return 400
    args_str = " ".join(args).split(";")

    group_number = int(args_str[0])
    proposals = list(map(lambda i: i.strip(), args_str[1:]))

    storekeeper = context.bot_data['storekeeper']
    selection = context.bot_data['selection']

    storekeeper_code = storekeeper.get_current_selection_code()

    if storekeeper_code == 200:
        await update.message.reply_text(f"Мне некуда добавить вашу Идею. Добавьте новую Выборку.")

        return storekeeper_code

    selection_code = selection.add_proposals(update.effective_user.mention_html(), group_number, proposals)

    if selection_code == 0:
        await update.message.reply_text(f"Ваши Идеи приняты!")

    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return selection_code


# Команда перемешивания очередности пользователей
@debug_print_return_code
async def shuffle_users_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат: /shuffle_order

    selection = context.bot_data['selection']

    selection_code = selection.shuffle_users_order()

    if selection_code == 0:
        await update.message.reply_html(f"Текущий порядок:\n{selection.answer_string}")
    elif selection_code == 200:
        await update.message.reply_text("Мне некого перемешивать")
    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return selection_code


# Команда извлечения Идеи следующего пользователя в очереди из Выборки
@debug_print_return_code
async def choose_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /choose

    selection = context.bot_data['selection']

    selection_code = selection.choose()

    if selection_code == 0:
        await update.message.reply_text(f"Выбираю: «{selection.answer_string}»")
    elif selection_code == 404:
        await update.message.reply_text("Похоже текущая Выборка опустела.")
    elif selection_code == 508:
        await update.message.reply_text(
            "Похоже в Выборке остались Идеи неопознанного мною пользователя. Пожалуйста, "
            "обозначьте себя (введите /add_me)"
        )
    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return selection_code


# Команда инициализации нового пользователя
@debug_print_return_code
async def add_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Формат /add_me

    storekeeper = context.bot_data['storekeeper']

    storekeeper_code = storekeeper.initialize_user(update.effective_user.mention_html())

    if storekeeper_code == 0:
        await update.message.reply_html(f"Привет! Теперь я тебя запомнил, {update.effective_user.mention_html()}!")
    elif storekeeper_code == 204:
        await update.message.reply_html(
            f"Я помню тебя, {update.effective_user.mention_html()}. Инициализация не требуется."
        )
    else:
        await update.message.reply_text(f"Пу-пу-пу, что-то пошло не так, извините:/")

    return storekeeper_code
