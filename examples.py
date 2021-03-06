from tornado import web

from sprockets.http import app, mixins, run


class StatusHandler(mixins.ErrorLogger, mixins.ErrorWriter,
                    web.RequestHandler):
    """Example that exercises the mix-ins in this library."""

    def get(self, status_code):
        """
        Returns the requested status.

        :param int status_code: the status code to return
        :queryparam str reason: optional reason phrase

        """
        status_code = int(status_code)
        if status_code >= 400:
            kwargs = {'status_code': status_code}
            if self.get_query_argument('reason', None):
                kwargs['reason'] = self.get_query_argument('reason')
            if self.get_query_argument('log_message', None):
                kwargs['log_message'] = self.get_query_argument('log_message')
            self.send_error(**kwargs)
        else:
            self.set_status(status_code)


class Application(app.Application):

    def __init__(self, **kwargs):
        kwargs['debug'] = True
        super(Application, self).__init__(
            [web.url(r'/status/(?P<status_code>\d+)', StatusHandler)],
            **kwargs)


if __name__ == '__main__':
    run(Application)
