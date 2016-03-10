# coding=utf8
#


from wheel.core.admin import create_admin
from wheel.core.app import WheelApp
from wheel.core.middleware import HTTPMethodOverrideMiddleware
from wheel.ext import configure_extensions


admin = create_admin()


def create_app_base(config=None, test=False, admin_instance=None, **settings):
    """ create a new app instance """
    app = WheelApp("wheel")
    app.config.load_wheel_config(config=config, test=test, **settings)
    if test or app.config.get('TESTING'):
        app.testing = True

    return app


def create_app(config=None, test=False, admin_instance=None, **settings):
    """ create the real app """
    app = create_app_base(config=config, test=test,
                          admin_instance=admin_instance, **settings)

    configure_extensions(app, admin_instance or admin)
    if app.config.get("HTTP_PROXY_METHOD_OVERRIDE"):
        app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app

