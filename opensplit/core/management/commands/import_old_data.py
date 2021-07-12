import sys
from unicodedata import normalize
from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
from django.utils.crypto import get_random_string
from opensplit.core.models import Expense, Organization
from opensplit.user.models import User
from collections import namedtuple


class Command(BaseCommand):
    help = "Import data from the old database"

    def handle(self, *args, **kwargs):
        # self.ImportUser()
        # self.ImportGroups()
        # self.ImportUserGroupRelation()
        self.ImportExpenses()
        self.ImportUserExpenseRelation()

    def ImportUser(self):
        count = 0
        columns = "id, email, name"
        UserRecord = namedtuple("UserRecord", columns)
        with connections["import"].cursor() as cursor:
            cursor.execute(f"select {columns} from user;")
            result = map(UserRecord._make, cursor.fetchall())
            for r in result:
                if r.name in ["x", ""]:
                    # filter weird entries
                    continue
                model = User(
                    legacy_id=r.id,
                    username=r.name,
                    email=r.email,
                    password=get_random_string(16),
                )
                model.save()
                count += 1
        print(f"Created {count} user")

    def ImportGroups(self):
        count = 0
        columns = "id, name, owner"
        OrganizationRecord = namedtuple("OrganizationRecord", columns)
        with connections["import"].cursor() as cursor:
            cursor.execute(f"select {columns} from 'group';")
            result = map(OrganizationRecord._make, cursor.fetchall())
            for r in result:
                if r.name in ("", "test", "https://app.openspl.it/invite/ezu7ok41b5ckb1taeh309o5fwmqfaw"):
                    # filter out weird groups
                    continue
                model = Organization(
                    legacy_id=r.id,
                    name=r.name,
                    token=get_random_string(12),
                    owner=User.objects.get(legacy_id=r.owner),
                )
                model.save()
                count += 1
        print(f"Created {count} organizations")

    def ImportUserGroupRelation(self):
        count = 0
        columns = "user_id, group_id"
        OrganizationRecord = namedtuple("OrganizationRecord", columns)
        with connections["import"].cursor() as cursor:
            cursor.execute(f"select {columns} from group_assoc;")
            result = map(OrganizationRecord._make, cursor.fetchall())
            for r in result:
                if r.group_id in [7, 11, 13, 14]:
                    continue
                org = Organization.objects.get(legacy_id=r.group_id)
                user = User.objects.get(legacy_id=r.user_id)
                org.member.add(user)
                count += 1
        print(f"Added {count} users into a organization")

    def ImportExpenses(self):
        count = 0
        columns = "id, description, amount,date,is_payment,group_id,paid_by"
        ExpenseRecord = namedtuple("ExpenseRecord", columns)
        with connections["import"].cursor() as cursor:
            cursor.execute(f"select {columns} from expense;")
            result = map(ExpenseRecord._make, cursor.fetchall())
            for r in result:
                model = Expense(
                    legacy_id=r.id,
                    description=r.description,
                    amount=r.amount / 100,
                    created_at=r.date,
                    organization=Organization.objects.get(legacy_id=r.group_id),
                    payment=bool(r.is_payment),
                    paid_by=User.objects.get(legacy_id=r.paid_by),
                )
                model.save()
                count += 1
        print(f"Created {count} expenses")

    def ImportUserExpenseRelation(self):
        count = 0
        columns = "user_id, expense_id"
        ExpenseRecord = namedtuple("ExpenseRecord", columns)
        with connections["import"].cursor() as cursor:
            cursor.execute(f"select {columns} from expense_assoc;")
            result = map(ExpenseRecord._make, cursor.fetchall())
            for r in result:
                try:
                    exp = Expense.objects.get(legacy_id=r.expense_id)
                except:
                    print(f"Expense with legacy_id {r.expense_id} got deleted in the DB")
                user = User.objects.get(legacy_id=r.user_id)
                exp.participants.add(user)
                count += 1
        print(f"Added {count} users to an expense")
