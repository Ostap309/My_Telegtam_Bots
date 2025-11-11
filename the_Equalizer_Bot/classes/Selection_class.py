import numpy as np
import pandas as pd
from random import choice as random_choice


class Selection:
    class ProposalSequence:
        def __init__(self, group: int, proposals: list) -> None:
            self.group: int = group
            self.queue: list = proposals

        def add(self, proposal: str) -> None:
            self.queue.append(proposal)

        def extract_first(self) -> str:
            return self.queue.pop(0)

        def is_empty(self) -> bool:
            return len(self.queue) == 0

        def __str__(self) -> str:
            return "\n   ◦ ".join(map(lambda i: f"|[Очередь {self.group}]| " + i, self.queue))

        def __add__(self, other):
            if self.group == other.group:
                return Selection.ProposalSequence(self.group, self.queue + other.queue)

            return self

        def __eq__(self, other):
            if isinstance(other, Selection.ProposalSequence) and self.group == other.group:
                return True

            return False

    def __init__(self, storekeeper):
        self.storekeeper = storekeeper
        self.proposals_dict = {}
        self.answer_string = ""

        self.refresh()

    def refresh(self) -> int:
        self.proposals_dict = {}

        for index, proposal in self.storekeeper.proposals_df.iterrows():
            if proposal["Selection"] == self.storekeeper.current_selection:
                self.dict_smart_add(proposal)

        return 0

    def dict_smart_add(self, proposal: pd.Series) -> int:
        user: str = proposal["User"]
        proposal_title: str = proposal["Proposal"]
        group: int = proposal["Group"]

        if user not in self.proposals_dict.keys():
            self.proposals_dict[user] = []

        if group == 0:
            self.proposals_dict[user].append(proposal_title)
        else:
            i = 0
            new_proposal = self.ProposalSequence(group, [proposal_title])
            for prop in self.proposals_dict[user]:
                if isinstance(prop, self.ProposalSequence) and prop == new_proposal:
                    self.proposals_dict[user][i] += new_proposal
                    return 0
                i += 1

            # Если ProposalSequence с совпадающей группой не найдет
            self.proposals_dict[user].append(new_proposal)

    def show_proposals(self) -> int:
        self.answer_string = "\n".join(
            [f"🗣️ {user} предложил(а):\n   • "
             + "\n   • ".join([str(prop) for prop in self.proposals_dict[user]])
             + "\n"
             for user in self.proposals_dict.keys()
             ]
        )

        if self.answer_string:
            return 0
        else:
            return 200

    def add_proposals(self, user: str, group_index: int, proposals: list) -> int:

        proposals_number = len(proposals)

        new_proposals_df = pd.DataFrame({
            'Selection': [self.storekeeper.current_selection] * proposals_number,
            'User': [user] * proposals_number,
            'Proposal': proposals,
            'Group': [group_index] * proposals_number
        })

        self.storekeeper.proposals_df = pd.concat([self.storekeeper.proposals_df,
                                                   new_proposals_df],
                                                  ignore_index=True
                                                  )
        self.refresh()

        return 0

    def choose(self) -> int:
        def shift_df_up(df: pd.DataFrame) -> pd.DataFrame:
            shifted_df = pd.DataFrame(
                np.roll(df.values, shift=-1, axis=0),
                columns=df.columns,
                index=df.index
            )
            return shifted_df

        if self.proposals_dict and not self.storekeeper.users_df.empty:
            selected_user: pd.Series = self.storekeeper.users_df.iloc[0]["User"]
            iter_num = 0
            while selected_user not in self.proposals_dict.keys():
                if iter_num > 100:
                    return 508
                self.storekeeper.users_df = shift_df_up(self.storekeeper.users_df)

                selected_user = self.storekeeper.users_df.iloc[0]["User"]

                iter_num += 1

            selected_user_proposals_list: list = self.proposals_dict[selected_user]
            selected_proposal = random_choice(selected_user_proposals_list)

            if isinstance(selected_proposal, self.ProposalSequence):
                self.answer_string: str = selected_proposal.extract_first()
                group_index = selected_proposal.group

                if selected_proposal.is_empty():
                    selected_user_proposals_list.remove(selected_proposal)

            else:
                self.answer_string: str = selected_proposal
                selected_user_proposals_list.remove(selected_proposal)
                group_index = 0

            self.storekeeper.proposals_df = self.storekeeper.proposals_df[
                ~((self.storekeeper.proposals_df["Selection"] == self.storekeeper.current_selection)
                  & (self.storekeeper.proposals_df["User"] == selected_user)
                  & (self.storekeeper.proposals_df["Proposal"] == self.answer_string)
                  & (self.storekeeper.proposals_df["Group"] == group_index))
            ]

            if not selected_user_proposals_list:
                del self.proposals_dict[selected_user]

            self.storekeeper.users_df = shift_df_up(self.storekeeper.users_df)

            return 0

        else:
            return 404

    def shuffle_users_order(self) -> int:
        shuffled_users_df = self.storekeeper.users_df.sample(frac=1).reset_index(drop=True)
        if shuffled_users_df.empty:
            return 200

        self.storekeeper.users_df = shuffled_users_df

        self.answer_string = " -> ".join(self.storekeeper.users_df["User"].to_list())

        return 0
