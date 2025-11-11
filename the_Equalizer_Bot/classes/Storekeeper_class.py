import pandas as pd
from the_Equalizer_Bot.config import DATA_PATH


class Storekeeper:
    def __init__(self) -> None:
        self.selection_df = pd.read_excel(DATA_PATH, sheet_name="Selections")
        self.proposals_df = pd.read_excel(DATA_PATH, sheet_name="Proposals")
        self.users_df = pd.read_excel(DATA_PATH, sheet_name="Users")

        self.all_selections_list = []
        self.current_selection = ""

        self.set_current_selection()

    def get_all_selections(self) -> int:
        self.all_selections_list = self.selection_df["Selection"].to_list()
        if self.all_selections_list:
            return 0
        else:
            return 200

    def add_selection(self, selection_name: str) -> int:
        if selection_name in self.all_selections_list:
            return 409

        new_selection_df = pd.DataFrame({
            'Selection': selection_name,
            'Current': 0
        }, index=[0])

        self.selection_df = pd.concat([self.selection_df, new_selection_df], ignore_index=True)
        self.set_current_selection(selection_name)

        return 0

    def undo(self) -> int:
        self.selection_df = pd.read_excel(DATA_PATH, sheet_name="Selections")
        self.proposals_df = pd.read_excel(DATA_PATH, sheet_name="Proposals")
        self.users_df = pd.read_excel(DATA_PATH, sheet_name="Users")

        self.set_current_selection()

        return 0

    def save(self) -> int:
        try:
            with pd.ExcelWriter(DATA_PATH, engine='openpyxl') as writer:
                self.selection_df.to_excel(writer, sheet_name="Selections", index=False)
                self.proposals_df.to_excel(writer, sheet_name="Proposals", index=False)
                self.users_df.to_excel(writer, sheet_name="Users", index=False)

            return 0
        except PermissionError:
            return 403

    def get_current_selection_code(self) -> int:
        if self.current_selection:
            return 0
        else:
            return 200

    def set_current_selection(self, selection_name: str = "") -> int:
        self.get_all_selections()
        current = self.selection_df[self.selection_df["Current"] == 1]

        if selection_name:
            if selection_name in self.all_selections_list:
                if not current.empty:
                    self.selection_df.loc[self.selection_df["Current"] == 1, "Current"] = 0
                self.selection_df.loc[self.selection_df["Selection"] == selection_name, "Current"] = 1
                self.current_selection = selection_name

            else:
                return 404
        else:
            if self.all_selections_list:
                if not current.empty:
                    self.current_selection = current["Selection"].iloc[0]
                else:
                    col_current_pos = self.selection_df.columns.get_loc("Current")
                    self.selection_df.iloc[0, col_current_pos] = 1
                    self.current_selection = self.all_selections_list[0]

            else:
                self.current_selection = ""

        return 0
