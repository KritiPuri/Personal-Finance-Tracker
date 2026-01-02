"""
Script to add sample expense data for testing
Run with: python manage.py shell < add_sample_expenses.py
Or: python add_sample_expenses.py (if django setup is configured)
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personalfinance.settings')
django.setup()

from django.contrib.auth.models import User
from expenses.models import Expense
from datetime import datetime, timedelta
import random

# Get the user
username = 'Allstrix'
user = User.objects.get(username=username)

# Sample expense data with realistic categories and amounts
sample_expenses = [
    ('Coffee', 'food', 5.50),
    ('Gym membership', 'fitness', 50.00),
    ('Taxi to work', 'transportation', 15.00),
    ('Lunch at restaurant', 'food', 25.00),
    ('Netflix subscription', 'entertainment', 12.99),
    ('Grocery shopping', 'groceries', 85.50),
    ('Pizza delivery', 'food', 22.00),
    ('Gas station', 'fuel', 45.00),
    ('Metro card', 'transportation', 30.00),
    ('Dinner with friends', 'food', 60.00),
    ('Phone bill', 'utilities', 55.00),
    ('Internet bill', 'utilities', 70.00),
    ('Movie tickets', 'entertainment', 28.00),
    ('Haircut', 'personal care', 25.00),
    ('Books', 'education', 35.00),
    ('Snacks', 'food', 12.50),
    ('Breakfast', 'food', 18.00),
    ('Uber ride', 'transportation', 20.00),
    ('Shopping clothes', 'shopping', 120.00),
    ('Medicine', 'health', 40.00),
    ('Dentist appointment', 'health', 150.00),
    ('Electricity bill', 'utilities', 95.00),
    ('Spotify subscription', 'entertainment', 9.99),
    ('Coffee shop', 'food', 7.50),
    ('Fast food', 'food', 15.00),
    ('Parking fee', 'transportation', 10.00),
    ('Rent payment', 'housing', 1200.00),
    ('Vegetables from market', 'groceries', 30.00),
    ('Fruits', 'food', 20.00),
    ('Ice cream', 'food', 8.00),
]

# Add expenses for the last 60 days
print(f"Adding sample expenses for user: {username}")
today = datetime.now().date()
added_count = 0

for i in range(60):
    # Get random date within last 60 days
    expense_date = today - timedelta(days=i)
    
    # Add 1-3 random expenses per day
    num_expenses = random.randint(1, 3)
    
    for _ in range(num_expenses):
        description, category, base_amount = random.choice(sample_expenses)
        
        # Add some randomness to amounts (±20%)
        amount = base_amount * random.uniform(0.8, 1.2)
        amount = round(amount, 2)
        
        # Create expense
        expense = Expense.objects.create(
            owner=user,
            description=description,
            category=category,
            amount=amount,
            date=expense_date
        )
        added_count += 1

print(f"✅ Successfully added {added_count} sample expenses!")
print(f"Date range: {today - timedelta(days=59)} to {today}")
print(f"\nTotal expenses in database for {username}: {Expense.objects.filter(owner=user).count()}")
print(f"\nYou can now:")
print(f"  - View expenses at: http://127.0.0.1:8000/")
print(f"  - View forecast at: http://127.0.0.1:8000/forecast/")
print(f"  - Test category prediction at: http://127.0.0.1:8000/add-expense")
