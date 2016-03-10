# coding=utf8
#

from wheel.core.wheel_themes import Themes


def configure(app):
    themes = Themes()
    themes.init_themes(app, app_identifier="wheel")
