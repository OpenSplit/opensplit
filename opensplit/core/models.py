from django.db import models
from django.conf import settings
from django.urls import reverse
from opensplit.user.models import User
from django.core.validators import MinValueValidator
from random import shuffle
from decimal import Decimal
from .helper import OrganizationDebts
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime


class Organization(models.Model):
    class Meta:
        unique_together = [["name", "owner"]]

    name = models.CharField(max_length=60)
    token = models.CharField(max_length=12)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    member = models.ManyToManyField(User)
    legacy_id = models.IntegerField(null=True)

    def __str__(self):
        return f"Org '{self.name}'"

    def recalculate(self):
        shares = Share.objects.filter(expense__organization=self).all()

        # Clear all old debts
        Debt.objects.filter(organization=self).all().delete()

        tmp = OrganizationDebts(self)
        for s in shares:
            tmp.add_debt(s.creditor, s.debtor, s.amount)

        # for d in tmp.get_debts():
        #     print(f"{d.amount}€ from {d.debtor} to {d.creditor}")
        Debt.objects.bulk_create(tmp.get_debts())

    def get_relevant_debts(self, user):
        debts = {"creditor": [], "debtor": []}
        for d in self.debts.all():
            if d.creditor == user:
                debts["creditor"].append(d)
            elif d.debtor == user:
                debts["debtor"].append(d)

        return debts

    @property
    def invite_link(self):
        return f"{settings.BASE_URL}{reverse('organization-join', args=(self.token,))}"


class Expense(models.Model):
    class Meta:
        ordering = ("-created_at",)

    description = models.CharField(max_length=240)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="expenses")
    paid_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    created_at = models.DateTimeField(default=datetime.now)
    participants = models.ManyToManyField(User)
    payment = models.BooleanField(default=False)
    legacy_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.description}"

    def print_participants(self):
        return ",".join([p.username for p in self.participants.all()])

    def split(self):
        cents = int(self.amount * 100)
        # Alle shares löschen für diese expense
        self.shares.all().delete()

        # split für jeden + rest
        count = len(self.participants.all())
        # print(f"Count: {count}")
        share = cents // count
        # print(f"Share: {share}")
        rest = cents - (count * share)
        # print(f"Rest: {rest}")

        debts = []
        # Jeder bezahlt erstmal das gleiche
        for _ in range(count):
            debts.append(share)

        # Den Rest fair verteilen
        for i in range(rest):
            debts[i] = debts[i] + 1

        # print(f"debts: {debts}")

        # shuffle debts and zip to participants
        shuffle(debts)
        for user, amount in zip(self.participants.all(), debts):

            if user == self.paid_by:
                # You can't owe money to yourself
                continue

            # print(f"{user} for {amount}")
            s = Share(
                amount=Decimal(amount / 100),
                debtor=user,
                creditor=self.paid_by,
                expense=self,
            )
            s.save()

        # when we resplit an expense we need to update the debts of an organization
        self.organization.recalculate()


@receiver(post_delete, sender=Expense)
def clear_shares(sender, instance, *args, **kwargs):
    # Clear all shares from this expense
    instance.shares.all().delete()
    # Calculate new debts in the organization
    instance.organization.recalculate()


class Share(models.Model):
    """
    DEBTOR owns AMOUNT money to the CREDTIOR
    """

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    debtor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    creditor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="shares")

    def __str__(self):
        return f"Split for exp. '{self.expense.id}'"


class Debt(models.Model):
    """
    DEBTOR owns AMOUNT money to the CREDTIOR
    """

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    debtor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="my_debts")
    creditor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="my_credits")
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="debts")

    def __str__(self):
        return f"Debt between {self.debtor.username} and {self.creditor.username}"
