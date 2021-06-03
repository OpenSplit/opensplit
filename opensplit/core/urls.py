from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("organization/<int:id>", views.organization, name="organization"),
    path("expense/<int:id>/delete", views.expense_delete,name="expense-delete"),
]
