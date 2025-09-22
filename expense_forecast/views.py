from django.shortcuts import render
import numpy as np
import pandas as pd
from django.utils.timezone import now
from expenses.models import Expense
from django.contrib import messages
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required

# NEW: use Holt/Winters
from statsmodels.tsa.holtwinters import ExponentialSmoothing

@login_required(login_url='/authentication/login')
def forecast(request):
    # Fetch more history to stabilize the model (e.g., last 180 expenses or last 180 days)
    expenses_qs = Expense.objects.filter(owner=request.user).order_by('-date')[:180]
    expenses = list(expenses_qs)

    if len(expenses) < 10:
        messages.error(request, "Not enough expenses to make a forecast. Please add more expenses.")
        return render(request, 'expense_forecast/index.html')

    # Build DataFrame
    df = pd.DataFrame({
        'Date': [e.date for e in expenses],
        'Amount': [float(e.amount) for e in expenses],
        'Category': [getattr(e, 'category', 'Unknown') for e in expenses],
    })

    # Ensure datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # ---- IMPORTANT: make true daily series (no interpolation of spend) ----
    # Sum multiple expenses on the same day; fill missing days with 0 spend.
    daily = (
        df.set_index('Date')['Amount']
          .groupby(pd.Grouper(freq='D'))
          .sum()
          .asfreq('D', fill_value=0.0)
    )

    # Simple descriptive per-category totals (historical). If you want per-category *forecast*,
    # you’d run a model per category; for now, keep what you had.
    category_forecasts = (
        df.groupby('Category')['Amount'].sum().to_dict()
    )

    # ---- Modeling: Holt-Winters on daily totals ----
    # Use weekly seasonality if we have enough data; otherwise use simple exponential smoothing.
    forecast_steps = 30
    has_weekly = len(daily) >= 28  # need at least ~4 weeks for seasonality to be meaningful

    try:
        if has_weekly:
            # additive trend, additive weekly seasonality tends to work for small, non-negative series
            model = ExponentialSmoothing(
                daily,
                trend='add',
                seasonal='add',
                seasonal_periods=7,
                initialization_method='estimated'
            )
        else:
            # fallback: simple smoothing without seasonality
            model = ExponentialSmoothing(
                daily,
                trend=None,
                seasonal=None,
                initialization_method='estimated'
            )

        fit = model.fit(optimized=True, use_brute=True)
        fc = fit.forecast(forecast_steps)
    except Exception:
        # very defensive: in case the fit fails, fall back to a naive forecast (last 7d mean)
        baseline = max(daily.tail(min(7, len(daily))).mean(), 0.0)
        fc = pd.Series([baseline] * forecast_steps,
                       index=pd.date_range(start=daily.index[-1] + pd.Timedelta(days=1),
                                           periods=forecast_steps, freq='D'))

    # Enforce non-negative predictions
    fc = fc.clip(lower=0.0)

    # Prepare outputs for template
    forecast_index = fc.index
    forecast_data = pd.DataFrame({'Date': forecast_index, 'Forecasted_Expenses': fc.values})
    forecast_data_list = forecast_data.reset_index(drop=True).to_dict(orient='records')

    # Total forecast for next 30 days
    total_forecasted_expenses = float(fc.sum())

    # Plot: history + forecast
    plt.figure(figsize=(10, 6))
    plt.plot(daily.index, daily.values, label='Previous Daily Expenses')
    plt.plot(forecast_index, fc.values, label='Forecasted Expenses (next 30 days)')
    plt.xlabel('Date')
    plt.ylabel('Expenses')
    plt.title('Expense Forecast for Next 30 Days')
    plt.legend()
    plot_file = 'static/img/forecast_plot.png'
    plt.savefig(plot_file, bbox_inches='tight')
    plt.close()

    context = {
        'forecast_data': forecast_data_list,
        'total_forecasted_expenses': total_forecasted_expenses,
        'category_forecasts': category_forecasts,
    }
    return render(request, 'expense_forecast/index.html', context)
