from .base import *

# Database / S3

DB_PATH = os.path.join(ROOT_DIR, '.config_secret/dev.json')
aws_value = json.loads(open(DB_PATH).read())

for key, value in aws_value.items():
    setattr(sys.modules[__name__], key, value)

# S3 FileStorage
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'

# AWS Storage
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
