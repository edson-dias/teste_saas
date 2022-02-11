import os


def get_postgres_configs():
    db_config = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get('DB_HOST'),
            "USER": os.environ.get('DB_USER'),
            "PASSWORD": os.environ.get('DB_PASSWORD'),
            "HOST": os.environ.get('DB_HOST'),
            "PORT": os.environ.get('DB_PORT'),
        }
    }
    return db_config


def get_django_secret():
    secret = os.environ.get('DJANGO_SECRET')
    return secret
