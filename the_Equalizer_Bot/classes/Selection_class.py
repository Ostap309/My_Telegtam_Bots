import pandas as pd


class Selection:
    class ProposalSequence:
        def __init__(self, group: int, proposals: list) -> None:
            self.group = group
            self.queue = proposals

        def add(self, proposal: str) -> None:
            self.queue.append(proposal)

        def drop(self) -> None:
            self.queue.pop(0)

        def __str__(self) -> str:
            return "\n   ◦ ".join(map(lambda i: f"|[Очередь {self.group}]| " + i, self.queue))

        def __add__(self, other):
            if self.group == other.group:
                return Selection.ProposalSequence(self.group, self.queue + other.queue)

            return self

        def __eq__(self, other):
            if self.group == other.group:
                return True

            return False

    def __init__(self, storekeeper):
        self.storekeeper = storekeeper
        self.proposals_dict = {}

        self.refresh()

    def refresh(self):
        self.proposals_dict = {}

        for index, proposal in self.storekeeper.proposals_df.iterrows():
            if proposal["Selection"] == self.storekeeper.current_selection:
                self.dict_smart_add(proposal)

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

    def show_proposals(self) -> str:
        return "\n".join(
            [f"🗣️ {user} предложил(а):\n   • "
             + "\n   • ".join([str(prop) for prop in self.proposals_dict[user]])
             + "\n"
             for user in self.proposals_dict.keys()
             ]
        )

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

        return 0
