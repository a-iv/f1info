# -*- coding: utf-8 -*-
from django.db import connection
from django.template import Template, Context
import traceback
import logging

# get root logger
logger = logging.getLogger()
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class ConsoleExceptionMiddleware:
    def process_exception(self, request, exception):
        import sys
        exc_info = sys.exc_info()
        print "######################## Exception #############################"
        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        print "################################################################"
        #print repr(request)
        #print "################################################################"


class SQLLogMiddleware:

    def process_response (self, request, response):
        time = 0.0
        for q in connection.queries:
            time += float(q['time'])
        t = Template(u'''
Total query count: {{ count }}
Total execution time: {{ time }}
{% for sql in sqllog %}
    {{ forloop.counter }}. {{ sql.time }}: {{ sql.sql|safe }}
{% endfor %}
        ''')

        if len(connection.queries):
            print u"######################## SQL Log###############################"
            print t.render(Context({
                'sqllog': connection.queries,
                'count': len(connection.queries),
                'time': str(time),
            }))
            print u"################################################################"

        return response


class ErrorLogMiddleware(object):
    def process_exception(self, request, exception):
        import sys
        exc_info = sys.exc_info()
        traceback_text = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        url = request.build_absolute_uri()
        error_msg = url + '\n' + str(traceback_text) + '\n'
        logging.error(error_msg)
