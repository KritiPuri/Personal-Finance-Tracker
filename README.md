# 💰 Personal Finance Tracker

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.1-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, AI-powered Django web application for managing personal finances with intelligent expense categorization, machine learning-based forecasting, and comprehensive financial analytics.

## 🚀 Live Demo  
Check out the live project: [Personal Finance Tracker](https://personal-finance-tracker-production-636a.up.railway.app/authentication/login/?next=/)

---

## ✨ Key Features

### 📊 **Expense & Income Management**
- ➕ Add, edit, delete, and categorize expenses and income
- 🔍 Smart search and filtering capabilities
- 📈 Visual dashboards with interactive charts
- 💾 Export data to CSV and Excel formats
- 📄 Generate detailed PDF reports

### 🤖 **AI-Powered Category Prediction**
- ⚡ Real-time expense category prediction as you type
- 🎯 Machine learning model trained on 335+ expense patterns
- 🧠 Intelligent text preprocessing with NLTK
- 🔄 Auto-updates with new expense patterns

### 📈 **Expense Forecasting**
- 🔮 30-day expense forecasting using time series analysis
- 📊 Visual trend analysis with matplotlib charts
- 🎯 Weekly seasonality detection
- 📉 Historical spending pattern analysis

### 👤 **User Management**
- 🔐 Secure authentication and registration
- 👥 Multi-user support with isolated data
- ⚙️ Customizable user preferences
- 📱 Responsive design for all devices

### 🛠️ **REST API**
- 🌐 RESTful API endpoints for integration
- 🔌 Easy third-party integration
- 📡 JSON-based data exchange

---

## 🧠 Machine Learning Models

This project leverages multiple machine learning models for intelligent financial insights:

### 1. **Expense Category Prediction**

#### **TF-IDF Vectorizer** (Text Feature Extraction)
- **Library:** `sklearn.feature_extraction.text.TfidfVectorizer`
- **Purpose:** Converts expense descriptions into numerical feature vectors
- **Why:** Transforms text like "gym membership" into mathematical representations that ML models can understand
- **How it works:**
  - Analyzes word frequency across all expense descriptions
  - Assigns importance scores to words (rare words get higher scores)
  - Creates sparse vectors representing text semantics

#### **Random Forest Classifier** (Category Prediction)
- **Library:** `sklearn.ensemble.RandomForestClassifier`
- **Configuration:** 100 decision trees (`n_estimators=100`)
- **Purpose:** Predicts expense category based on description
- **Why Random Forest:**
  - ✅ Handles small datasets well (trained on 335 examples)
  - ✅ Resistant to overfitting through ensemble learning
  - ✅ Fast predictions (< 100ms)
  - ✅ No need for extensive hyperparameter tuning
  - ✅ Works well with TF-IDF features
- **Training Data:** `dataset.csv` with 335 expense examples across 30+ categories
- **Accuracy:** High accuracy on common expense types (food, transportation, utilities, etc.)

#### **Cosine Similarity** (Semantic Matching)
- **Library:** `sklearn.metrics.pairwise.cosine_similarity`
- **Purpose:** Finds most similar expense in training data
- **Why:** Improves predictions by identifying closest matching historical expenses
- **Formula:** Measures angle between user input vector and training vectors

#### **NLTK** (Natural Language Processing)
- **Library:** `nltk` (Natural Language Toolkit)
- **Components Used:**
  - `word_tokenize`: Splits text into individual words
  - `stopwords`: Removes common words ("the", "a", "is", etc.)
- **Purpose:** Cleans and preprocesses expense descriptions
- **Why:**
  - ✅ Removes noise from text
  - ✅ Improves model accuracy by focusing on meaningful words
  - ✅ Standardizes text format (lowercase, alphanumeric)
- **Example:** "I purchased new gym equipment" → "purchased new gym equipment"

**Category Prediction Workflow:**
```
User Input: "pizza delivery"
    ↓
NLTK Preprocessing → "pizza delivery" (cleaned)
    ↓
TF-IDF Vectorization → [0.0, 0.87, 0.0, ..., 0.45]
    ↓
Cosine Similarity → Finds similar training examples
    ↓
Random Forest → Predicts category: "food"
    ↓
Returns: {"predicted_category": "food", "confidence": 0.92}
```

---

### 2. **Expense Forecasting**

#### **Holt-Winters Exponential Smoothing** (Time Series Forecasting)
- **Library:** `statsmodels.tsa.holtwinters.ExponentialSmoothing`
- **Purpose:** Forecasts daily expenses for the next 30 days
- **Why Holt-Winters:**
  - ✅ Captures **trend** (increasing/decreasing spending over time)
  - ✅ Detects **seasonality** (weekly spending patterns)
  - ✅ Works with sparse data (gaps in spending days)
  - ✅ Fast computation for real-time predictions
  - ✅ Industry-standard for financial forecasting
- **Configuration:**
  - **Trend Component:** Additive (linear trend)
  - **Seasonal Component:** Additive with 7-day period (weekly patterns)
  - **Initialization:** Estimated from historical data
  - **Optimization:** Brute-force search for best parameters
- **Training Data:** Last 180 expenses (approximately 60 days)
- **Forecast Horizon:** 30 days ahead
- **Fallback Strategy:** If model fails to converge, uses 7-day moving average

**Forecasting Workflow:**
```
User's Expense History (60 days)
    ↓
Data Preprocessing:
  - Group by date
  - Fill missing days with $0
  - Create daily time series
    ↓
Holt-Winters Model Training:
  - Detect weekly seasonality (if 28+ days available)
  - Estimate trend component
  - Optimize smoothing parameters
    ↓
Generate 30-Day Forecast
    ↓
Post-Processing:
  - Clip negative values to $0
  - Calculate total predicted expense
  - Generate visualization plot
    ↓
Returns: Forecasted amounts + confidence intervals
```

---

## 🛠️ Technology Stack

### **Backend**
- **Framework:** Django 5.1.1
- **Language:** Python 3.12+
- **Database:** SQLite (dev), PostgreSQL-ready (production)
- **API:** Django REST Framework 3.15.2

### **Machine Learning**
- **scikit-learn 1.5.1:** ML models and preprocessing
- **statsmodels 0.14.2:** Time series forecasting
- **NLTK 3.9.1:** Natural language processing
- **pandas 2.2.2:** Data manipulation
- **numpy 2.1.1:** Numerical computations

### **Visualization**
- **matplotlib 3.9.2:** Chart generation
- **Chart.js:** Interactive frontend charts

### **Frontend**
- **Bootstrap 5:** Responsive UI framework
- **JavaScript (ES6+):** Interactive features
- **HTML5/CSS3:** Modern web standards

### **Deployment**
- **Gunicorn 21.2.0:** WSGI HTTP server
- **Whitenoise 6.5.0:** Static file serving
- **Railway:** Cloud hosting platform

---

## 📦 Installation & Setup
### **Prerequisites**
- Python 3.12 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv/virtualenv)

### **Quick Start**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KritiPuri/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (required for category prediction):**
   ```bash
   python nltk_downloader.py
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional - for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Start development server:**
   ```bash
   # With debug mode
   python manage.py runserver
   
   # Or set environment variables
   set DEBUG=True
   set ALLOWED_HOSTS=localhost,127.0.0.1
   python manage.py runserver
   ```

9. **Access the application:**
   - Main App: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Endpoints: http://127.0.0.1:8000/api/

---

## 📁 Project Structure

```
Personal-Finance-Tracker/
├── 📂 api/                      # REST API endpoints
│   ├── views.py                # Category prediction & dataset updates
│   ├── urls.py                 # API routing
│   └── serializers.py          # Data serialization
│
├── 📂 authentication/          # User authentication
│   ├── views.py                # Login, logout, registration
│   └── urls.py                 # Auth routing
│
├── 📂 expense_forecast/        # ML-based forecasting
│   ├── views.py                # Holt-Winters forecasting logic
│   └── templates/              # Forecast visualization pages
│
├── 📂 expenses/                # Expense management
│   ├── models.py               # Expense & Category models
│   ├── views.py                # CRUD operations
│   └── templates/              # Expense UI templates
│
├── 📂 userincome/              # Income tracking
│   ├── models.py               # Income & Source models
│   └── views.py                # Income management
│
├── 📂 userpreferences/         # User settings
│   └── models.py               # Currency preferences
│
├── 📂 userprofile/             # User profiles
│   ├── models.py               # Profile model
│   └── forms.py                # Profile forms
│
├── 📂 report_generation/       # PDF report generation
│   ├── tasks.py                # Background report tasks
│   └── views.py                # Report generation logic
│
├── 📂 personalfinance/         # Django project settings
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
│
├── 📂 static/                  # Static assets
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── img/                    # Images & charts
│
├── 📂 templates/               # HTML templates
│   ├── base.html               # Base template
│   ├── expenses/               # Expense templates
│   ├── income/                 # Income templates
│   └── partials/               # Reusable components
│
├── 📄 dataset.csv              # ML training data (335 examples)
├── 📄 manage.py                # Django management script
├── 📄 requirements.txt         # Python dependencies
├── 📄 nltk_downloader.py       # NLTK data installer
├── 📄 add_sample_expenses.py   # Sample data generator
└── 📄 README.md                # This file
```

---

## 🎯 Key Workflows

### **1. Adding an Expense with AI Category Prediction**

-User types description → JavaScript debounces input (500ms)
-AJAX POST to /api/predict-category/
-NLTK preprocessing → TF-IDF vectorization
-Random Forest prediction → Category auto-filled

**Implementation:**
- Frontend: `templates/expenses/add_expense.html` (JavaScript with debouncing)
- Backend: `api/views.py` → `PredictCategory` class
- Model training: On-demand with `dataset.csv`

### **2. Generating 30-Day Expense Forecast**

```mermaid
flowchart TD
   A[User visits /forecast/] --> B[Load last 180 expenses]
   B --> C[Group by date + fill missing days]
   C --> D[Detect weekly seasonality]
   D --> E[Train Holt-Winters model]
   E --> F[Generate 30-day forecast]
   F --> G[Create matplotlib chart]
   G --> H[Display predictions]
```

**Implementation:**
- View: `expense_forecast/views.py` → `forecast` function
- Model: Holt-Winters Exponential Smoothing
- Visualization: matplotlib saved to `static/img/forecast_plot.png`

---

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file or set system environment variables:

```bash
# Development settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Production settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Secret key (change in production!)
SECRET_KEY=your-secret-key-here
```

### **Static Files**

For production deployment:
```bash
python manage.py collectstatic --noinput
```

Static files are served using **Whitenoise** with compressed manifest storage.

---

## 🧪 Testing

### **Run Test Suite**
```bash
python manage.py test
```

### **Test Coverage by Module**
- ✅ Authentication (login, register, logout)
- ✅ Expense CRUD operations
- ✅ Income tracking
- ✅ Category prediction API
- ✅ Forecast generation
- ✅ User preferences

### **Manual Testing Checklist**
- [ ] User registration and login
- [ ] Add/edit/delete expenses
- [ ] Category prediction while typing
- [ ] View expense dashboard with charts
- [ ] Generate 30-day forecast
- [ ] Export data to CSV/PDF
- [ ] Income tracking
- [ ] User profile management

---

## 🚀 Deployment

### **Railway Deployment (Recommended)**

1. **Connect your GitHub repository to Railway**
2. **Set environment variables:**
   ```
   DEBUG=False
   ALLOWED_HOSTS=your-app.up.railway.app
   CSRF_TRUSTED_ORIGINS=https://your-app.up.railway.app
   ```
3. **Railway automatically detects:**
   - `Procfile` for Gunicorn server
   - `runtime.txt` for Python version
   - `requirements.txt` for dependencies

4. **Database migrations run automatically via `railway.json`**

### **Manual Deployment Steps**

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start Gunicorn server
gunicorn personalfinance.wsgi:application --bind 0.0.0.0:8000
```

---

## 📊 Screenshots
| Dashboard | Expense Management | Category Prediction |
|-----------|-------------------|---------------------|
| ![image1f](outputs/image1f.png) | ![image2f](outputs/image2f.png) | ![image3f](outputs/image3f.png) |

| Forecasting | Analytics | Reports |
|-------------|-----------|---------|
| ![image5f](outputs/image5f.png) | ![image6f](outputs/image6f.png) | ![image7f](outputs/image7f.png) |

| Income Tracking | User Profile | Settings |
|----------------|--------------|----------|
| ![image8f](outputs/image8f.png) | ![image9f](outputs/image9f.png) | |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Code Style**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features

---

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature idea? Please open an issue on GitHub with:
- Clear description of the problem/feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots (if applicable)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Kriti Puri** - *Initial work* - [GitHub](https://github.com/KritiPuri)

---

## 🙏 Acknowledgments

- **Django** - Web framework
- **scikit-learn** - Machine learning library
- **statsmodels** - Time series forecasting
- **NLTK** - Natural language processing
- **Bootstrap** - UI framework
- **Chart.js** - Data visualization
- **Railway** - Hosting platform

---

## 📚 Additional Resources

### **Documentation**
- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [statsmodels Time Series](https://www.statsmodels.org/stable/tsa.html)
- [NLTK Documentation](https://www.nltk.org/)

### **Tutorials & Guides**
- [How to Train ML Models for Text Classification](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- [Time Series Forecasting with Python](https://www.statsmodels.org/stable/examples/notebooks/generated/exponential_smoothing.html)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)

---

## 🔮 Future Enhancements

- [ ] **Multi-currency support** with real-time exchange rates
- [ ] **Budget alerts** via email/SMS notifications
- [ ] **Category-specific forecasting** (predict per category)
- [ ] **Receipt scanning** with OCR technology
- [ ] **Mobile app** (React Native/Flutter)
- [ ] **Recurring expenses** automation
- [ ] **Bill reminders** and payment tracking
- [ ] **Financial goals** tracker
- [ ] **Investment portfolio** integration
- [ ] **Advanced analytics** with Pandas Profiling
- [ ] **Model persistence** (cache trained ML models)
- [ ] **ARIMA/SARIMA** alternative forecasting models
- [ ] **Deep learning** for improved predictions

---

## 💡 Tips & Best Practices

### **For Better Category Predictions:**
- Add diverse examples to `dataset.csv`
- Use consistent naming in descriptions
- Include common spending patterns
- The model learns from your data!

### **For Accurate Forecasts:**
- Add expenses regularly (daily is best)
- Include all spending (even small amounts)
- Maintain at least 30 days of history
- More data = better predictions

### **Performance Optimization:**
- Cache trained ML models (future enhancement)
- Use database indexes on frequently queried fields
- Optimize static file delivery with CDN
- Enable database query caching

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

*Empowering you to take control of your finances!* 💰📊

Made with ❤️ using Django & Machine Learning

</div>
