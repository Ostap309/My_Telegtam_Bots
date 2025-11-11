from config import *
from bot_functions import *

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from classes.Storekeeper_class import Storekeeper
from classes.Selection_class import Selection

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Настройка работы бота
def main() -> None:
    # Создайте приложение и передайте ему токен вашего бота.
    application = Application.builder().token(BOT_TOKEN).build()
    storekeeper = Storekeeper()
    selection = Selection(storekeeper)

    application.bot_data['storekeeper'] = storekeeper
    application.bot_data['selection'] = selection

    for command in BOT_COMMANDS:
        # command[0] - Имя команды, command[1] - Имя функции, реализующей команду
        application.add_handler(CommandHandler(command[0], command[1]))

    # on non command, т.е. сообщение - повторить сообщение в Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускайте бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
