import opensplit.core.models


class OrganizationDebts:
    def __init__(self, org):
        self.organization = org
        self.debts = []

    def add_debt(self, creditor, debtor, amount):
        forward = None

        # check if we have a forward facing debt
        for d in self.debts:
            if d.creditor == creditor and d.debtor == debtor:
                forward = d

        if forward:
            # If we found one, add the mount
            forward.amount += amount
        else:
            # if we found none, create a new one
            forward = opensplit.core.models.Debt(
                creditor=creditor, organization=self.organization, debtor=debtor, amount=amount
            )
            self.debts.append(forward)

        backward = None
        # check if we have a backward facing debt
        for d in self.debts:
            if d.creditor == debtor and d.debtor == creditor:
                backward = d

        if backward:
            common_amount = min(forward.amount, backward.amount)
            for direction in [forward, backward]:
                direction.amount -= common_amount
                if direction.amount == 0:
                    self.debts.remove(direction)

        else:
            # don't have to do anything in this case
            pass

    def get_debts(self):
        return self.debts
