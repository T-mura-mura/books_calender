from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,

#      'loggers': {
#          'django': {
#              'handlers': ['console'],
#              'level': 'INFO',
#          },
#          'hello': {
#              'handlers': ['console'],
#              'level': 'DEBUG',
#          },
#      },
#      'handlers': {
#          'console': {
#              'level': 'DEBUG',
#              'class': 'Logging.StreamHandler',
#              'formatter': 'dev',
#          },
#      },
#      'formatters': {
#          'dev': {
#              'format': '\t'.join([
#                  '%(asctime)s',
#                  '[%(levelname)s]',
#                  '%(pathname)s(Line:%(lineno)d)',
#                  '%(message)s'
#              ])
#          },
#      }
# }