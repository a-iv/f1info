
from f1info.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

MIDDLEWARE_CLASSES += [
    'f1info.middleware.ConsoleExceptionMiddleware',
]
