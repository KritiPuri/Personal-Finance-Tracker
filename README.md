
# Personal Finance Tracker


🚀 **Live Demo:** [personal-finance-tracker-production-636a.up.railway.app](https://personal-finance-tracker-production-636a.up.railway.app)

A modern, full-featured Django web application for managing personal finances, tracking expenses, forecasting budgets, and generating insightful reports.

## Features

- User authentication and secure registration
- Add, edit, and categorize expenses and income
- Visual dashboards with charts and analytics
- Expense forecasting using machine learning
- PDF report generation and data export
- User preferences and profile management
- REST API endpoints for integration
- Responsive UI with custom styling

## Getting Started

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KritiPuri/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Download NLTK data:**
   ```bash
   python nltk_downloader.py
   ```
5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```
8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

## Project Structure

```
Personal-Finance-Tracker/
├── api/
├── authentication/
├── expense_forecast/
├── expenses/
├── personalfinance/           # Main project settings
├── report_generation/
├── static/
├── templates/
├── userincome/
├── userpreferences/
├── userprofile/
├── manage.py
├── requirements.txt
├── Pipfile
├── ...
```


*Empowering you to take control of your finances!*
