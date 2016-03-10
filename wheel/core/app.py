# coding=utf8
#


from flask import Flask
from flask import Blueprint
from flask.helpers import _endpoint_from_view_func
from wheel.core.config import WheelConfig
from wheel.utils.aliases import dispatch_aliases


class WheelApp(Flask):
    """
    Implementes customizations on Flask
    - Config handler
    - Aliases dispatching before request
    """

    config_class = WheelConfig

    def make_config(self, instance_relative=False):
        """This method should be removed when Flask is >=0.11"""
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)

    def preprocess_request(self):
        return dispatch_aliases() or super(WheelApp,
                                           self).preprocess_request()

    def add_wheel_url_rule(self, rule, endpoint=None,
                            view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        if not endpoint.startswith('wheel.'):
            endpoint = 'wheel.core.' + endpoint
        self.add_url_rule(rule, endpoint, view_func, **options)


class WheelModule(Blueprint):
    "Overwrite blueprint namespace to wheel.modules.name"

    def __init__(self, name, *args, **kwargs):
        name = "wheel.modules." + name
        super(WheelModule, self).__init__(name, *args, **kwargs)
