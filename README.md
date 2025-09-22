## 📸 Outputs


Below are output images (located in the `outputs/` folder):

| Output 1 | Output 2 | Output 3 |
|----------|----------|----------|
| ![image1f](outputs/image1f.png) | ![image2f](outputs/image2f.png) | ![image3f](outputs/image3f.png) |
| Output 5 | Output 6 | Output 7 |
| ![image5f](outputs/image5f.png) | ![image6f](outputs/image6f.png) | ![image7f](outputs/image7f.png) |
| Output 8 | Output 9 | |
| ![image8f](outputs/image8f.png) | ![image9f](outputs/image9f.png) | |





# Personal Finance Tracker


## 🚀 Live Demo  
Check out the live project here: [Personal Finance Tracker](https://personal-finance-tracker-production-636a.up.railway.app/authentication/login/?next=/  )


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
