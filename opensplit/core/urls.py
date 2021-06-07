from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("organization/<int:id>", views.organization, name="organization"),
    path("organization/<int:id>/expense", views.organization_expense, name="organization-expense"),
    path("organization/<int:id>/payment", views.organization_payment, name="organization-payment"),
    path("join/<token>", views.organization_join, name="organization-join"),
    path("expense/<int:id>/delete", views.expense_delete, name="expense-delete"),
    path("expense/<int:id>/edit", views.expense_edit, name="expense-edit"),
]
