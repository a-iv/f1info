#import rpdb2; rpdb2.start_embedded_debugger('1')

from f1info.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

MIDDLEWARE_CLASSES += [
    'f1info.middleware.ConsoleExceptionMiddleware',
]
