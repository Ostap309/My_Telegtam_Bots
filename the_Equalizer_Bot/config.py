import bot_functions

# Значение токена
BOT_TOKEN = "8317649438:AAE4vcBtcc7NgX1RtRAii1u0ApkDT_m6wF8"
# Путь к таблицам с данными
DATA_PATH = "Data\\data.xlsx"

# Список команд и их реализаций
BOT_COMMANDS = [("start", bot_functions.start_command),
                ("help", bot_functions.help_command),
                ("add_selection", bot_functions.add_selection_command),
                ("get_all_selections", bot_functions.get_all_selections_command),
                ("save", bot_functions.save_command),
                ("undo", bot_functions.undo_command),
                ("current", bot_functions.current_selection_command),
                ("set_current", bot_functions.set_current_selection_command),
                ("get_all_proposals", bot_functions.get_all_proposals_command),
                ("add_proposals", bot_functions.add_proposals_command),
                ("shuffle_order", bot_functions.shuffle_users_order_command),
                ("choose", bot_functions.choose_command),
                ("add_me", bot_functions.add_me_command)
                ]
