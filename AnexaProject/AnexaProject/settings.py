from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import cloudinary


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR.parent, '.env'))
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}


SECRET_KEY = 'django-insecure-b63y%q+&wn7n4s&30!uwv3$yvgn7z!i7@m(6v$o08fc5#_0bu6'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Yeh line add karein
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AnexaProject.urls'
AUTH_USER_MODEL = 'main_app.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AnexaProject.wsgi.application'


# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


### Render

# DATABASES = {
#     'default': dj_database_url.parse(
#         "postgresql://anexafacedsdb_user:N9U0CsAugbgcW3vwxOtHM3lBK0dovhx4@dpg-dadptnf40ujc73ch4kk0-a.oregon-postgres.render.com/anexafacedsdb",
#         conn_max_age=600,
#         ssl_require=True
#     )
# }



# https://console.neon.tech/app/projects/late-sun-90503737?database=neondb
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://neondb_owner:npg_XHcsn0lCkrV2@ep-cool-cloud-ay8yxwd3-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
        conn_max_age=600,
        ssl_require=True
    )
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'shaneepandey123@gmail.com'
# EMAIL_HOST_PASSWORD = 'mdpv rqhj offz xhrd'

# DEFAULT_FROM_EMAIL = 'ANEXA Facade Systems <shaneepandey123@gmail.com>'
# SERVER_EMAIL = 'shaneepandey123@gmail.com'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'info@anexafacade.com'
# EMAIL_HOST_PASSWORD = 'ibwi lsly ubmr ybie'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'ANEXA Facade Systems <info@anexafacade.com>'
SERVER_EMAIL = 'info@anexafacade.com'







# Step 5: Git Cache se Purani 60+ MB Images Kaise Hatayein? (Zaroori Step)
# Kyunki images pehle hi commit ho chuki hain, sirf .gitignore me likhne se purani images Git se delete nahi hoti. Unko Git cache se hatane ke liye VS Code terminal me yeh commands chalaayein:

# Static images ko Git tracking se remove karein (Aapki files computer se delete nahi hongi, sirf Git se hatengi):

# Bash
# git rm -r --cached main_app/static/images
# (Agar staticfiles bhi track ho gaya ho to: git rm -r --cached staticfiles)

# Check karein ki .env to track nahi ho rahi:
# git rm --cached .env
# (Agar "fatal: pathspec did not match" aaye toh tension mat lein, matlab .env safe hai).

# Ab Git me commit karein:

# Bash
# git add .gitignore
# git commit -m "Removed heavy static images from git tracking and added .env"
# Ab Render/GitHub par push karein:

# Bash
# git push origin main
# Ab push 2 second me fast chala jayega kyunki 60+ MB ki images Git chhod chuka hai!

# Step 6: Render par Setting
# Kyunki .env file ko humne security ke liye Git par push nahi kiya hai, isliye Render Dashboard par jaana hoga:

# Render Dashboard me apni Web Service open karein.

# Left menu me Environment par click karein.

# Add Environment Variable click karke wahi 3 keys daal dein:

# CLOUDINARY_CLOUD_NAME = your_actual_cloud_name

# CLOUDINARY_API_KEY = your_actual_api_key

# CLOUDINARY_API_SECRET = your_actual_api_secret

# Save Changes kar dein.



### for db
# https://console.neon.tech/app/projects/late-sun-90503737/branches/br-muddy-hall-ay25kivv/tables
# pip install gunicorn whitenoise
# pip freeze > requirements.txt

# ALLOWED_HOSTS = ['*']
# pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
# gunicorn AnexaProject.wsgi:application

# cd ..
# git init
# git add .
# git commit -m "Initial commit - ANEXA Project setup"
# git branch -M main
# git remote add origin https://github.com/Shanipandey8545/AnexaProject.git
# git push -u origin main




# after every changes 
# cd ..
# git add .
# git commit -m "Add gunicorn and whitenoise for render deployment"
# git push origin main