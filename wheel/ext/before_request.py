# coding=utf8
#


def configure(app):
    @app.before_first_request
    def initialize():
        app.logger.info("Called only once, when the first request comes in")
