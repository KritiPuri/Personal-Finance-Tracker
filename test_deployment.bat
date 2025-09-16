@echo off
echo 🚀 WINDOWS DEPLOYMENT TEST
echo ========================

echo.
echo 🔄 Testing Django configuration...
python manage.py check
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Django check failed!
    exit /b 1
)

echo.
echo 🔄 Testing Django deployment check...
python manage.py check --deploy
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Deployment check has warnings
)

echo.
echo 🔄 Testing imports...
python -c "import django, nltk, matplotlib, pandas, sklearn; print('✅ All imports successful')"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Import test failed!
    exit /b 1
)

echo.
echo 🔄 Testing WSGI...
python -c "from personalfinance.wsgi import application; print('✅ WSGI application loaded successfully')"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ WSGI test failed!
    exit /b 1
)

echo.
echo 🔄 Testing static files collection...
python manage.py collectstatic --noinput
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Static files collection failed!
    exit /b 1
)

echo.
echo 🔄 Testing migrations...
python manage.py migrate --noinput
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Migration failed!
    exit /b 1
)

echo.
echo 🔄 Testing NLTK data...
python -c "import nltk; nltk.data.find('tokenizers/punkt'); nltk.data.find('corpora/stopwords'); print('✅ NLTK data available')"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ NLTK data test failed!
    exit /b 1
)

echo.
echo ✅ ALL TESTS PASSED! Ready for deployment! 🚀
echo.
echo To deploy now, run:
echo git add .
echo git commit -m "All tests passed - ready for deployment"
echo git push -f origin main