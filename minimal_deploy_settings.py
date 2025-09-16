# Minimal settings changes for deployment only
import os
from pathlib import Path
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-#e(g$@-wfcc07s^4avvl4ls)fx1uo-3p=gp9ol5w5g(!0k*0r4'

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# ... rest of settings remain the same