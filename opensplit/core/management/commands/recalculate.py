import sys
from django.core.management.base import BaseCommand
from opensplit.core.models import Expense, Share, Organization, Debt


class Command(BaseCommand):
    help = "Recalculate all shares and debts"

    def handle(self, *args, **kwargs):
        self.clear()
        self.calculateShares()
        self.calculateDebts()

    def clear(self):
        Share.objects.all().delete()
        Debt.objects.all().delete()

    def calculateShares(self):
        for e in Expense.objects.all():
            print(f"Splitting expense '{e}'")
            e.split()

    def calculateDebts(self):
        for o in Organization.objects.all():
            print(f"Calculating debts for organization '{o}'")
            o.recalculate()
