# Импорт конфигурации
from config import *
# Импорт функционала бота
from bot_functions import *

# Импорт основных библиотек (логирование и телеграм-боты)
import logging
from telegram.ext import Application, CommandHandler

# Импорт классов-обработчиков
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
    # Создание объектов Приложение (с передачей токена), Кладовщик и Выборка (с указанием Кладовщика)
    application = Application.builder().token(BOT_TOKEN).build()
    storekeeper = Storekeeper()
    selection = Selection(storekeeper)

    # Записываем Кладовщика и Выборку в данные бота, чтобы обеспечить корректную работу функций бота
    application.bot_data['storekeeper'] = storekeeper
    application.bot_data['selection'] = selection

    # Передаем боту список команд
    for command in BOT_COMMANDS:
        # command[0] - Имя команды, command[1] - Имя функции, реализующей команду
        application.add_handler(CommandHandler(command[0], command[1]))

    # Запускает бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
