from .base import *

# Static & Media files

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')

MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# Database

DB_PATH = os.path.join(ROOT_DIR, '.config_secret/local.json')
db_value = json.loads(open(DB_PATH).read())

for key, value in db_value.items():
    setattr(sys.modules[__name__], key, value)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
