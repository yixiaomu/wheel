# coding=utf8
#


import os
import logging
import wheel.core.models as m

from flask.config import Config
from wheel.utils import parse_conf_data
from cached_property import cached_property
from cached_property import cached_property_ttl


logger = logging.getLogger()


class WheelConfig(Config):
    """
        A config object for flask that tries to ger vers from
        database and then from config itself
    """
    
    @cached_property
    def store(self):
        return dict(self)

    @cached_property_ttl(300)
    def all_settings_from_db(self):
        """
            As config reads data from database on every app.config.get(key)/[key]
            this data is cached as cached_property
        """
        try:
            return {item.name: item.value
                    for item in m.config.Config.objects.get(
                        group='settings').values}
        except Exception as msg:
            logger.warning("Error reading all settings from db: %s" % msg)
            return {}

    def get_from_db(self, key, default=None):
        return self.all_settings_from_db.get(key, default)

    def __getitem__(self, key):
        return self.get_from_db(key) or dict.__getitem__(self, key)

    def get(self, key, default=None):
        return self.get_from_db(key) or self.store.get(key) or default

    def from_object(self, obj, silent=False):
        try:
            super(WheelConfig, self).from_object(obj)
        except ImportError as msg:
            if silent:
                return False
            msg.message = "Unable to load configuration obj (%s)" % msg.message
            raise

    def from_envvar_namespace(self, namespace="WHEEL", silent=False):
        try:
            data = {key.partition('_')[-1]: parse_conf_data(data)
                    for key, data
                    in os.environ.items()
                    if key.startswith(namespace)}
            self.update(data)
        except Exception as msg:
            if silent:
                return False
            msg.message = "Unable to load config env namespace (%s)" % msg.message
            raise

    def load_wheel_config(self, config=None, mode=None, test=None, **sets):
        self.from_object(config or 'wheel.settings')
        mode = mode or "test" if test else os.environ.get("WHEEL_MODE", "local")
        self.from_object("wheel.%s_settings" % mode, silent=True)
        path = "WHEEL_SETTINGS" if not test else "WHEELTEST_SETTINGS"
        self.from_envvar(path, silent=True)
        self.from_envvar_namespace(namespace="WHEEL", silent=True)
        self.update(sets)