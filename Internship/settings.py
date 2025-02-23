import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-626n111s2_tcbpqp64ni_k$s35wqxzht7_9gxqpd*m10m_75!6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Installed Apps 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'MyAdmin',
    'Users',
]

# Crispy Form
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

# Auth and Redirect Urls
AUTH_USER_MODEL = 'Users.UserModel'
LOGIN_REDIRECT_URL = 'Home'
LOGOUT_REDIRECT_URL = 'Home'
LOGIN_URL = 'StudentLogin'

# Email Details
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your SMTP server
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'devpunjani2123@gmail.com' 
EMAIL_HOST_PASSWORD = 'vvmz bhlz epcq idyf'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'MyAdmin.middleware.MyAdminMiddleware', 
]

ROOT_URLCONF = 'Internship.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Users', 'templates'), # app1's templates directory
            os.path.join(BASE_DIR, 'MyAdmin', 'templates'), # app2's templates directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Internship.wsgi.application'

# Database Details
DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
        'NAME': 'internship',
        'USER': 'root',
        'PASSWORD' : '',
        'HOST' : 'localhost',
        'PORT' : '3306'
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static Files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"Static"),
]
MEDIA_URL='/'
MEDIA_ROOT=os.path.join(BASE_DIR,'')

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'