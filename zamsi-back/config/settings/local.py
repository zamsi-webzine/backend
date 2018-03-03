from .base import *

# Database

DB_PATH = os.path.join(ROOT_DIR, '.config_secret/local.json')
db_value = json.loads(open(DB_PATH).read())

for key, value in db_value.items():
    setattr(sys.modules[__name__], key, value)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
