import bot_functions

# Значение токена
BOT_TOKEN = "8317649438:AAE4vcBtcc7NgX1RtRAii1u0ApkDT_m6wF8"
# Путь к таблицам с данными
DATA_PATH = "Data\\data.xlsx"

# Список команд и их реализаций
BOT_COMMANDS = [(("start", "st"), bot_functions.start_command),
                (("help", "h"), bot_functions.help_command),
                (("add_selection", "adds"), bot_functions.add_selection_command),
                (("get_all_selections", "gas"), bot_functions.get_all_selections_command),
                (("save", "sv"), bot_functions.save_command),
                (("undo", "u"), bot_functions.undo_command),
                (("current", "cur"), bot_functions.current_selection_command),
                (("set_current", "sc"), bot_functions.set_current_selection_command),
                (("get_all_proposals", "gap"), bot_functions.get_all_proposals_command),
                (("add_proposals", "addp"), bot_functions.add_proposals_command),
                (("shuffle_order", "shf"), bot_functions.shuffle_users_order_command),
                (("choose", "ch"), bot_functions.choose_command),
                (("add_me", "am"), bot_functions.add_me_command)
                ]
