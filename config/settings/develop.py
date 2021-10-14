"""
Configuraciones para el entorno de desarrollo o local.
"""
from .base import *  # noqa
from .base import env

# GENERAL
# ----------------------------------------------------------------------------
DEBUG = True

# LOGGING
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module}'
                      ' {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': False,
        },
        'services': {
            'handlers': ['console'],
            'propagate': False
        }
    }
}
