from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from datetime import datetime, date, timedelta
from io import BytesIO
import csv
import openpyxl
import json

from .models import Source, UserIncome
from expenses.models import Expense
from userpreferences.models import UserPreference
from django.template.loader import get_template
from xhtml2pdf import pisa


# --------------------------
# Search
# --------------------------
@login_required(login_url='/authentication/login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')
        income = (
            UserIncome.objects.filter(owner=request.user, amount__istartswith=search_str) |
            UserIncome.objects.filter(owner=request.user, date__istartswith=search_str) |
            UserIncome.objects.filter(owner=request.user, description__icontains=search_str) |
            UserIncome.objects.filter(owner=request.user, source__icontains=search_str)
        )
        data = income.values()
        return JsonResponse(list(data), safe=False)
    return JsonResponse([], safe=False)


# --------------------------
# List / Index
# --------------------------
@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.filter(owner=request.user)
    income = UserIncome.objects.filter(owner=request.user)

    sort_order = request.GET.get('sort')
    if sort_order == 'amount_asc':
        income = income.order_by('amount')
    elif sort_order == 'amount_desc':
        income = income.order_by('-amount')
    elif sort_order == 'date_asc':
        income = income.order_by('date')
    elif sort_order == 'date_desc':
        income = income.order_by('-date')

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = None

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'total': page_obj.paginator.num_pages,
        'sort_order': sort_order,
        'sources': sources,
    }
    return render(request, 'income/index.html', context)


# --------------------------
# Create
# --------------------------
@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.filter(owner=request.user)
    if len(sources) == 0:
        messages.info(request, "you need to add income sources first in order to add income")
        return HttpResponseRedirect('/account/')

    context = {'sources': sources, 'values': request.POST}

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date_str = request.POST.get('income_date')
        description = request.POST.get('description', '').strip()
        source = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        try:
            the_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            if the_date > today:
                messages.error(request, 'Date cannot be in the future')
                return render(request, 'income/add_income.html', context)

            UserIncome.objects.create(
                owner=request.user,
                amount=amount,
                date=the_date,
                source=source,
                description=description
            )
            messages.success(request, 'Income saved successfully')
            return redirect('income')

        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'income/add_income.html', context)


# --------------------------
# Update
# --------------------------
@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id, owner=request.user)
    sources = Source.objects.filter(owner=request.user)

    context = {'income': income, 'values': income, 'sources': sources}

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date_str = request.POST.get('income_date')
        description = request.POST.get('description', '').strip()
        source = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)

        try:
            the_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            if the_date > today:
                messages.error(request, 'Date cannot be in the future')
                return render(request, 'income/edit_income.html', context)

            income.amount = amount
            income.date = the_date
            income.source = source
            income.description = description
            income.save()

            messages.success(request, 'Income saved successfully')
            return redirect('income')

        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'income/edit_income.html', context)


# --------------------------
# Delete
# --------------------------
@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id, owner=request.user)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')


# --------------------------
# Income Summary (FIXED)
# --------------------------
@login_required(login_url='/authentication/login')
def income_summary(request):
    user = request.user

    # Convert to date because model uses DateField
    today_dt = timezone.now()
    today = today_dt.date()
    week_start = today - timedelta(days=6)  # last 7 days including today

    daily_income = user.userincome_set.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    weekly_income = user.userincome_set.filter(date__range=[week_start, today]).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_income = user.userincome_set.filter(date__year=today.year, date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_income = user.userincome_set.filter(date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'daily_income': daily_income,
        'weekly_income': weekly_income,
        'monthly_income': monthly_income,
        'yearly_income': yearly_income,
    }
    return render(request, 'income/dashboard.html', context)


# --------------------------
# Monthly data (JSON) — owner-scoped + aggregated
# --------------------------
@login_required(login_url='/authentication/login')
def monthly_income_data(request):
    current_year = datetime.now().year

    # Aggregate per month for the current user
    monthly_data_qs = (
        UserIncome.objects
        .filter(owner=request.user, date__year=current_year)
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total_income=Sum('amount'))
        .order_by('month')
    )

    monthly_income_data = [0] * 12
    for item in monthly_data_qs:
        month_index = (item['month'] or 0) - 1
        if 0 <= month_index < 12:
            monthly_income_data[month_index] = float(item['total_income'] or 0)

    return JsonResponse({'monthly_income_data': monthly_income_data})


# --------------------------
# Another monthly endpoint (fixed aggregation)
# --------------------------
@login_required(login_url='/authentication/login')
def get_monthly_income(request):
    today = date.today()
    first_day_of_year = today.replace(month=1, day=1)
    last_day_of_year = today.replace(month=12, day=31)

    # Proper aggregation instead of overwriting
    income_qs = (
        UserIncome.objects
        .filter(owner=request.user, date__range=(first_day_of_year, last_day_of_year))
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    monthly_data = [0] * 12
    for row in income_qs:
        m = (row['month'] or 0) - 1
        if 0 <= m < 12:
            monthly_data[m] = float(row['total'] or 0)

    return JsonResponse({'monthly_data': monthly_data})


# --------------------------
# PDF Export helper
# --------------------------
def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="expense_report.pdf"'
        return response
    return HttpResponse("Error rendering PDF", status=400)


# --------------------------
# Report / Exports (owner-scoped)
# --------------------------
@login_required(login_url='/authentication/login')
def export_pdf(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    incomes = UserIncome.objects.filter(owner=request.user, date__range=[start_date, end_date])
    expenses = Expense.objects.filter(owner=request.user, date__range=[start_date, end_date])

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expense

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render_to_pdf('income/pdf_template.html', context)


@login_required(login_url='/authentication/login')
def report(request):
    report_generated = False
    return render(request, 'income/report.html', {'report_generated': report_generated})


@login_required(login_url='/authentication/login')
def generate_report(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date > end_date:
            messages.error(request, "Start date cannot be greater than end date.")
            return redirect('report')

        incomes = UserIncome.objects.filter(owner=request.user, date__range=[start_date, end_date])
        expenses = Expense.objects.filter(owner=request.user, date__range=[start_date, end_date])

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        savings = total_income - total_expense

        context = {
            'incomes': incomes,
            'expenses': expenses,
            'total_income': total_income,
            'total_expense': total_expense,
            'savings': savings,
            'start_date': start_date,
            'end_date': end_date,
            'report_generated': True
        }
        return render(request, 'income/report.html', context)

    return render(request, 'income/report.html')


@login_required(login_url='/authentication/login')
def export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    incomes = UserIncome.objects.filter(owner=request.user, date__range=[start_date, end_date])
    expenses = Expense.objects.filter(owner=request.user, date__range=[start_date, end_date])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{start_date}_to_{end_date}.csv"'

    writer = csv.writer(response)

    # Income
    writer.writerow(['Income'])
    writer.writerow(['Date', 'Source', 'Amount'])
    income_total = 0
    for inc in incomes:
        writer.writerow([inc.date, inc.source, inc.amount])
        income_total += inc.amount
    writer.writerow(['', f'Total Income: {income_total}'])

    # Expenses
    writer.writerow(['Expenses'])
    writer.writerow(['Date', 'Category', 'Amount'])
    expense_total = 0
    for exp in expenses:
        writer.writerow([exp.date, exp.category, exp.amount])
        expense_total += exp.amount

    writer.writerow([])
    writer.writerow(['', f'Total Expenses: {expense_total}'])

    return response


@login_required(login_url='/authentication/login')
def export_xlsx(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    incomes = UserIncome.objects.filter(owner=request.user, date__range=[start_date, end_date])
    expenses = Expense.objects.filter(owner=request.user, date__range=[start_date, end_date])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="report_{start_date}_to_{end_date}.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active

    # Income
    ws.append(['Income'])
    ws.append(['Date', 'Source', 'Amount'])
    income_total = 0
    for inc in incomes:
        ws.append([inc.date, inc.source, inc.amount])
        income_total += inc.amount
    ws.append(['', f'Total Income: {income_total}'])

    # Expenses
    ws.append(['Expenses'])
    ws.append(['Date', 'Category', 'Amount'])
    expense_total = 0
    for exp in expenses:
        ws.append([exp.date, exp.category, exp.amount])
        expense_total += exp.amount

    ws.append([])
    ws.append(['', f'Total Expenses: {expense_total}'])

    wb.save(response)
    return response
