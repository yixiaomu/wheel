# coding=utf8
#


from flask import g
from babel.support import LazyProxy
from flask.ext.babelex import gettext
from flask.ext.babelex import lazy_gettext
from flask.ext.babelex import ngettext


def ugettext(s):
    return g.translations.ugettext(s)


ugettext_lazy = LazyProxy(ugettext)

_ = gettext
_l = lazy_gettext
_n = ngettext