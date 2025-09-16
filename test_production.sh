# Production-like Environment Variables for Testing
export DEBUG=False
export DJANGO_SETTINGS_MODULE=personalfinance.settings

# Test commands to run before deployment:
echo "Testing production-like environment..."

# 1. Check Django configuration
python manage.py check --deploy

# 2. Test static files
python manage.py collectstatic --noinput

# 3. Test migrations
python manage.py migrate --noinput

# 4. Test server startup
echo "Starting test server..."
python manage.py runserver 127.0.0.1:8001 &
SERVER_PID=$!

# Wait and test
sleep 5
curl -I http://127.0.0.1:8001/ || echo "Server test failed"

# Cleanup
kill $SERVER_PID

echo "Local tests completed!"