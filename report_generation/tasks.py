from celery import shared_task
from django.utils import timezone
from expenses.models import Expense
from userincome.models import UserIncome
from django.contrib.auth.models import User
import pandas as pd
import os


@shared_task
def generate_report():
    today = timezone.now()
    end_of_week = today - timezone.timedelta(days=today.weekday()) + timezone.timedelta(days=6)

    if today.day == end_of_week.day:  # If it's the last day of the week
        for user in User.objects.all():  # Loop through each user
            # Fetch weekly incomes
            weekly_incomes = UserIncome.objects.filter(date__range=[end_of_week - timezone.timedelta(days=6), end_of_week], owner=user)

            # Convert to DataFrame
            weekly_income_data = list(weekly_incomes.values('description', 'source', 'amount'))
            weekly_income_df = pd.DataFrame(weekly_income_data)

            # Save the report to an Excel file
            weekly_report_path = f'weekly_report_{user.username}.xlsx'
            with pd.ExcelWriter(weekly_report_path) as writer:
                weekly_income_df.to_excel(writer, sheet_name='Incomes', index=False)

    if today.day == 1:  # If it's the first day of the month
        for user in User.objects.all():  # Loop through each user
            # Fetch monthly incomes
            monthly_incomes = UserIncome.objects.filter(date__month=today.month, date__year=today.year, owner=user)

            # Convert to DataFrame
            monthly_income_data = list(monthly_incomes.values('description', 'source', 'amount'))
            monthly_income_df = pd.DataFrame(monthly_income_data)

            # Save the report to an Excel file
            monthly_report_path = f'monthly_report_{user.username}.xlsx'
            with pd.ExcelWriter(monthly_report_path) as writer:
                monthly_income_df.to_excel(writer, sheet_name='Incomes', index=False)
