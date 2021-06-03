from django.shortcuts import render, get_object_or_404, redirect
from .models import Organization, Expense
from .forms import ExpenseForm


def index(request):
    orgs = request.user.organization_set.all()
    return render(request, "core/index.pug", {"orgs": orgs})

def organization(request,id):
    org = get_object_or_404(Organization, pk=id)
    debts = org.get_relevant_debts(request.user)
    form = ExpenseForm(org=org)
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = Expense(
                description = form.cleaned_data["description"],
                amount = form.cleaned_data["amount"],
                paid_by = form.cleaned_data["paid_by"],
                organization = org,
            )
            exp.save()
            for x in form.cleaned_data["participants"]:
                exp.participants.add(x)
            # split after we added all participants
            exp.split()
            return redirect("organization", org.id)

    return render(request, "core/organization.pug", {"org": org, "form": form, "debts": debts})

def expense_delete(request, id):
    exp = get_object_or_404(Expense, pk=id)
    org =exp.organization
    exp.delete()
    return redirect("organization", org.id)
