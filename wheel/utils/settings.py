# coding=utf8
#


import logging
from flask import request
from flask import current_app
from wheel.core.db import db
from wheel.core import models as m
from wheel.core.app import WheelApp


logger = logging.getLogger()


def create_app_min(config=None, test=False):
    app = WheelApp('wheel')
    app.config.load_wheel_config(config=config, test=test)
    return app


def get_site_url():
    try:
        from_site_config = m.config.Config.get('site', 'site_domain', None)
        from_settings = get_setting_value('SERVER_NAME', None)
        if from_settings and not from_settings.startswith('http'):
            from_settings = 'http://%s/' % from_settings
        return from_site_config or from_settings or request.url_root
    except RuntimeError:
        return "http://localhost/"


def get_setting_value(key, default=None):
    try:
        return current_app.config.get(key, default)
    except RuntimeError as msg:
        logger.warning("current_app is inaccessible: %s" % str(msg))

    try:
        app = create_app_min()
        db.init_app(app)
        with app.app_context():
            return app.config.get(key, default)
    except:
        return default


def get_password(f):
    try:
        return open('.%s_password.txt' % f).read().strip()
    except:
        return