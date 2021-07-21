from django.contrib import admin
from .models import Organization, Expense, Share, Debt


def split_expense(modeladmin, request, queryset):
    for e in queryset:
        e.split()


split_expense.short_description = "Calculate the shares for this expense"


def calculate_debts(modeladmin, request, queryset):
    for o in queryset:
        o.recalculate()


calculate_debts.short_description = "Calculate debts between members"


class ExpenseAdmin(admin.ModelAdmin):
    actions = [split_expense]
    list_display = ["description", "organization", "created_at"]


class OrganizationAdmin(admin.ModelAdmin):
    actions = [calculate_debts]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Share)
admin.site.register(Debt)
