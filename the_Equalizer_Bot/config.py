import bot_functions

BOT_TOKEN = "8317649438:AAE4vcBtcc7NgX1RtRAii1u0ApkDT_m6wF8"
DATA_PATH = "Data\\data.xlsx"

BOT_COMMANDS = [("start", bot_functions.start_command),
                ("help", bot_functions.help_command),
                ("add_selection", bot_functions.add_selection_command),
                ("get_all_selections", bot_functions.get_all_selections_command),
                ("save", bot_functions.save_command),
                ("undo", bot_functions.undo_command)
                ]
