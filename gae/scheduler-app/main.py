import base64
import logging
import os
import urllib2
import webapp2

APP_ENGINE_CRON_HEADER = 'X-Appengine-Cron'
SCHEDULE_FUNCTION_URL_VAR = 'ScheduleFunctionUrl'
SCHEDULE_FUNCTION_USERNAME_VAR = 'ScheduleFunctionUsername'
SCHEDULE_FUNCTION_PASSWORD_VAR = 'ScheduleFunctionPassword'

AUTH_BASE64 = base64.b64encode('%s:%s' % (os.environ[SCHEDULE_FUNCTION_USERNAME_VAR],
                                          os.environ[SCHEDULE_FUNCTION_PASSWORD_VAR]))


class ScheduleRequestHandler(webapp2.RequestHandler):
    def get(self):
        try:
            if self.request.headers.get(APP_ENGINE_CRON_HEADER, False) != "true":
                raise ValueError('Not invoked from the task queue job')

            logging.debug('Request handler invoked from the task queue job')

            request = urllib2.Request(os.environ[SCHEDULE_FUNCTION_URL_VAR])
            request.add_header("Authorization", "Basic %s" % AUTH_BASE64)
            response = urllib2.urlopen(request)
            content = response.read()

            self.response.write(content)
        except:
            logging.exception('Failed processing request')
            self.response.status = 500


app = webapp2.WSGIApplication([('/schedule', ScheduleRequestHandler), ], debug=True)
