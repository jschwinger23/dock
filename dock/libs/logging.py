import logging
import logging.config

default_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[{asctime}][{levelname}]: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'dock': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

logging.config.dictConfig(default_config)

getLogger = logging.getLogger
