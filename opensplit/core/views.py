from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from .models import Organization, Expense
from .forms import ExpenseForm, NewOrgForm, PaymentForm


def index(request):
    if not request.user.is_authenticated:
        # Show welcome page instead of actual app
        return render(request, "core/home.pug")

    orgs = request.user.organization_set.all()
    form = NewOrgForm()
    if request.method == "POST":
        form = NewOrgForm(request.POST)
        if form.is_valid():
            org = Organization(name=form.cleaned_data["name"], owner=request.user, token=get_random_string(12))
            org.save()
            org.member.add(request.user)
            return redirect("organization", org.id)
    return render(request, "core/index.pug", {"orgs": orgs, "form": form})


@login_required
def organization(request, id):
    org = get_object_or_404(Organization, pk=id)
    if request.user not in org.member.all():
        return HttpResponseBadRequest()
    # debts = org.get_relevant_debts(request.user)
    return render(request, "core/organization.pug", {"org": org})


@login_required
def organization_join(request, token):
    org = get_object_or_404(Organization, token=token)

    # Redirect to the group if you are already a member
    if request.user in org.member.all():
        return redirect("organization", org.id)

    if request.method == "POST":
        org.member.add(request.user)
        return redirect("organization", org.id)
    return render(request, "core/organization-join.pug", {"org": org})


@login_required
def organization_expense(request, id):
    org = get_object_or_404(Organization, pk=id)
    form = ExpenseForm(org=org, initial={"paid_by": request.user})
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = Expense(
                description=form.cleaned_data["description"],
                amount=form.cleaned_data["amount"],
                paid_by=form.cleaned_data["paid_by"],
                organization=org,
            )
            exp.save()
            for x in form.cleaned_data["participants"]:
                exp.participants.add(x)
            # split after we added all participants
            exp.split()
            return redirect("organization", org.id)
    return render(request, "core/organization-expense.pug", {"org": org, "form": form})


@login_required
def organization_payment(request, id):
    org = get_object_or_404(Organization, pk=id)
    form = PaymentForm(org=org, initial={"sender": request.user})
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            exp = Expense(
                description=form.cleaned_data["description"],
                amount=form.cleaned_data["amount"],
                paid_by=form.cleaned_data["sender"],
                payment=True,
                organization=org,
            )
            exp.save()
            exp.participants.add(form.cleaned_data["receiver"])
            # split after we added all participants
            exp.split()
            return redirect("organization", org.id)
    return render(request, "core/organization-payment.pug", {"org": org, "form": form})


@login_required
def expense_delete(request, id):
    exp = get_object_or_404(Expense, pk=id)
    org = exp.organization
    exp.delete()
    return redirect("organization", org.id)


@login_required
def expense_edit(request, id):
    exp = get_object_or_404(Expense, pk=id)
    org = exp.organization
    form = ExpenseForm(org=org, instance=exp)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
        return redirect("organization", org.id)
    return render(request, "core/organization-expense.pug", {"org": org, "form": form})
