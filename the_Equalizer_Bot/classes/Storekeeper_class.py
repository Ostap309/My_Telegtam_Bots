import pandas as pd
from the_Equalizer_Bot.config import DATA_PATH


class Storekeeper:
    def __init__(self) -> None:
        self.selection_df = pd.read_excel(DATA_PATH, sheet_name="Selections")
        self.proposals_df = pd.read_excel(DATA_PATH, sheet_name="Proposals")
        self.users_df = pd.read_excel(DATA_PATH, sheet_name="Users")

    def get_all_selections(self) -> list:
        return self.selection_df["Selection"].to_list()

    def add_selection(self, selection_name: str) -> int:
        if selection_name in self.get_all_selections():
            return 409

        self.selection_df.loc[len(self.selection_df)] = selection_name

        return 0

    def undo(self) -> int:
        self.selection_df = pd.read_excel(DATA_PATH, sheet_name="Selections")
        self.proposals_df = pd.read_excel(DATA_PATH, sheet_name="Proposals")
        self.users_df = pd.read_excel(DATA_PATH, sheet_name="Users")

        return 0

    def save(self) -> int:
        with pd.ExcelWriter(DATA_PATH, engine='openpyxl') as writer:
            self.selection_df.to_excel(writer, sheet_name="Selections", index=False)
            self.proposals_df.to_excel(writer, sheet_name="Proposals", index=False)
            self.users_df.to_excel(writer, sheet_name="Users", index=False)

        return 0
