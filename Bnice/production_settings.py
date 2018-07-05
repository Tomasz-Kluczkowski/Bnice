from Bnice.common_settings import *  # noqa
from decouple import config
import dj_database_url

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
ALLOWED_HOSTS = ['b-nice-staging.herokuapp.com',
                 'b-nice.herokuapp.com']
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
