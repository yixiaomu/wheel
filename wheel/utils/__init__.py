# coding=utf8
#


import json

from flask import current_app
from speaklater import make_lazy_string

from flask.ext.security import current_user
from wheel.modules.accounts.models import User

import logging
logger = logging.getLogger()


def lazy_setting(key, default=None):
    return make_lazy_string(lambda: current_app.config.get(key, default))


def lazy_str_setting(key, default=None):
    return str(lazy_setting(key, default))


def get_current_user():
    try:
        return User.objects.get(id=current_user.id)
    except Exception as msg:
        logger.warning("No user found: %s", str(msg))
        return current_user


def get_current_user_for_models():
    user = get_current_user()
    try:
        if not user.is_authenticated():
            return None
        return user
    except Exception as msg:
        logger.info("Can't access is_authenticated method: %s" % str(msg))
        return None


def is_accessible(roles_accepted=None, user=None):
    user = user or get_current_user()
    if user.has_role('admin'):
        return True
    if roles_accepted:
        accessible = any(user.has_role(role) for role in roles_accepted)
        return accessible

    return True


def parse_conf_data(data):
    """
    @int @bool @ float @json (for lists and dicts)
    strings does not need converters

    export WHEEL_DEFAULT_THEME='marterial'
    export WHEEL_DEBUG='@bool True'
    export WHEEL_PAGINATION_PER_PAGE='@int 20'
    export WHEEL_MONGODB_SETTINGS='@json {"db": "wheel_db", "HOST": "mongo"}'
    """
    true_values = ('t', 'true', 'enabled', '1', 'on', 'yes')
    converters = {'@int': int,
                  '@float': float,
                  '@bool': lambda value: True if value.lower() in true_values else False,
                  '@json': json.loads}

    if data.startswith(tuple(converters.keys())):
        parts = data.partition(' ')
        converter_key = parts[0]
        value = parts[-1]
        return converters.get(converter_key)(value)

    return data