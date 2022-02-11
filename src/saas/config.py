import os


def get_postgres_configs():
    db_config = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('DB_HOST', 'postgres'),
            "USER": os.environ.get('DB_USER', 'postgres'),
            "PASSWORD": os.environ.get('DB_PASSWORD', 'developer123'),
            "HOST": os.environ.get('DB_HOST', 'localhost'),
            "PORT": os.environ.get('DB_PORT', '54321'),
        }
    }
    return db_config


def get_django_secret():
    secret = os.environ.get('DJANGO_SECRET')
    return secret
