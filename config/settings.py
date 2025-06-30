from pathlib import Path
import os
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$7rxo$xkm=bt*mt&5q50w+t&n*@q9^gx19$0d)hk*87b^wzu*9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "COMPONENT_SPLIT_REQUEST": True,
    # OTHER SETTINGS
}
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": "user123",
            "secret_key": "pass123123",
            "bucket_name": "my-bucket",
            "endpoint_url": "http://minio-storage:9000",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "import_export",
    # ------------------------
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # -------------------------
    "rest_framework",
    "rest_framework.authtoken",
    # -------------------------
    # "drf_yasg",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # -------------------------
    "apps.users",
    "apps.products",
    "apps.carts",
    "apps.orders",
    "apps.payment",
    # ---------------------------
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ec-db",
        "USER": "user",
        "PASSWORD": "pass123",
        # "HOST": "postgres-db",
        "HOST": os.getenv("DB_HOST", "ecommerce-postgres"),
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://ecommerce-redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "mysecret"
        },
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


def badge_callback(request):
    return 3


UNFOLD = {
    "SITE_TITLE": "Custom suffix in <title> tag",
    "SITE_HEADER": "UNFOLD DEMO",
    "DASHBOARD_CALLBACK": "apps.products.views.dashboard_callback",
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": "https://google.com",
        },
        {
            "icon": "diamond",
            "title": _("admin index"),
            "link": reverse_lazy("admin:index"),
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "badge": badge_callback,
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            }
        ],
    },
}
