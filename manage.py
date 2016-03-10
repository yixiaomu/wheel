# coding=utf8
#


import logging
import click
from wheel import create_app
from wheel.core.db import db


app = create_app()

if app.config.get("LOGGER_ENABLED"):
    logger.basicConfig(level=getattr(logging,
                                     app.config.get('LOGGER_LEVEL',
                                                    'DEBUG')),
                       format=app.config.get('LOGGER_FORMAT',
                                             '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
                       datefmt=app.config.get('LOGGER_DATE_FORMAT', '%d.%m %H:%M:%S'))


def runserver(reloader=True, debug=True, host='127.0.0.1', port=5000):
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


if __name__ == '__main__':
    runserver()
