#!/usr/bin/env python
# coding=utf8
#

from werkzeug.utils import import_string

from flask import request
from flask import session
from flask.ext.admin import Admin

from wheel.core.models.subcontent import SubContentPurpose
from wheel.core.models.config import Config
from wheel.core.models.channel import Channel
from wheel.core.models.channel import ChannelType
from wheel.core.models.content import Link
from wheel.core.models.content import ContentTemplateType

from wheel.utils.translation import _l
from wheel.utils.translation import _n
from wheel.utils.settings import get_setting_value

from wheel.core.admin.models import ModelAdmin
from wheel.core.admin.models import FileAdmin
from wheel.core.admin.models import BaseIndexView

from wheel.core.admin.views import IndexView
from wheel.core.admin.views import InspectorView
from wheel.core.admin.views import LinkAdmin
from wheel.core.admin.views import ConfigAdmin
from wheel.core.admin.views import SubContentPurposeAdmin
from wheel.core.admin.views import ChannelTypeAdmin
from wheel.core.admin.views import ContentTemplateTypeAdmin
from wheel.core.admin.views import ChannelAdmin


"""
_n is here only for backwards compatibility, to be imported by 3rd party
modules. The below _n below is to avoid pep8 error
"""
_n  # noqa


class WheelAdmin(Admin):
    registered = []

    def register(self, model, view=None, *args, **kwargs):
        _view = view or ModelAdmin
        admin_view_exclude = get_setting_value('ADMIN_VIEW_EXCLUDE', [])
        identifier = '.'.join((model.__module__, model.__name__))
        if (identifier not in admin_view_exclude) and (
                identifier not in self.registered):
            self.add_view(_view(model, *args, **kwargs))
            self.registered.append(identifier)


def create_admin(app=None):
    index_view = IndexView()
    return WheelAdmin(app, index_view=index_view)


def configure_admin(app, admin):  # noqa

    custom_index = app.config.get('ADMIN_INDEX_VIEW')
    if custom_index:
        admin.index_view = import_string(custom_index)()
        if isinstance(admin._views[0], BaseIndexView):
            del admin._views[0]
        admin._views.insert(0, admin.index_view)

    admin_config = app.config.get('ADMIN',
                                  {'name': 'Wheel Admin',
                                   'url': '/admin'})

    for k, v in list(admin_config.items()):
        setattr(admin, k, v)

    babel = app.extensions.get('babel')
    if babel:
        try:
            @babel.localeselector
            def get_locale():
                # use default language if set
                if app.config.get('BABEL_DEFAULT_LOCALE'):
                    session['lang'] = app.config.get('BABEL_DEFAULT_LOCALE')
                else:
                    # get best matching language
                    if app.config.get('BABEL_LANGUAGES'):
                        session['lang'] = request.accept_languages.best_match(
                            app.config.get('BABEL_LANGUAGES')
                        )

                return session.get('lang', 'en')

            admin.locale_selector(get_locale)
        except Exception as e:
            app.logger.info('Cannot add locale_selector. %s' % e)

    for entry in app.config.get('FILE_ADMIN', []):
        try:
            admin.add_view(
                FileAdmin(
                    entry['path'],
                    entry['url'],
                    name=_l(entry['name']),
                    category=_l(entry['category']),
                    endpoint=entry['endpoint'],
                    roles_accepted=entry.get('roles_accepted'),
                    editable_extensions=entry.get('editable_extensions')))
        except Exception as e:
            app.logger.info(e)

    # register all themes in file manager
    for k, theme in app.theme_manager.themes.items():
        try:
            if k == app.config.get('DEFAULT_THEME'):
                suffix = "(Site theme)"
            elif k == app.config.get('ADMIN_THEME'):
                suffix = "(Admin theme)"
            else:
                suffix = "Theme"

            admin.add_view(
                FileAdmin(
                    theme.static_path,
                    "/_themes/{0}/".format(theme.identifier),
                    name="{0}: {1} static files".format(suffix,
                                                        theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_static_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
            admin.add_view(
                FileAdmin(
                    theme.templates_path,
                    "/theme_template_files/{0}/".format(theme.identifier),
                    name="{0}: {1} template files".format(suffix,
                                                          theme.identifier),
                    category=_l("Files"),
                    endpoint="{0}_template_files".format(theme.identifier),
                    roles_accepted=('admin', "editor"),
                    editable_extensions=app.config.get(
                        'DEFAULT_EDITABLE_EXTENSIONS')
                )
            )
        except Exception as e:
            app.logger.warning(
                'Error registering %s folder to file admin %s' % (
                    theme.identifier, e
                )
            )

    # adding views
    # TODO uncomment
    #admin.add_view(InspectorView(category=_l("Settings"),
    #                             name=_l("Inspector")))

    # adding extra views
    extra_views = app.config.get('ADMIN_EXTRA_VIEWS', [])
    for view in extra_views:
        admin.add_view(
            import_string(view['module'])(
                category=_l(view.get('category')),
                name=_l(view.get('name'))
            )
        )

    # adding model views
    #admin.register(
    #    Link,
    #    LinkAdmin,
    #    category=_l("Content"),
    #    name=_l("Link")
    #)
    #admin.register(Config,
    #               ConfigAdmin,
    #               category=_l("Settings"),
    #               name=_l("Config"))
    #admin.register(SubContentPurpose,
    #               SubContentPurposeAdmin,
    #               category=_l("Settings"),
    #               name=_l("Sub content purposes"))
    #admin.register(ChannelType, ChannelTypeAdmin,
    #               category=_l("Settings"), name=_l("Channel type"))
    #admin.register(ContentTemplateType,
    #               ContentTemplateTypeAdmin,
    #               category=_l("Settings"),
    #               name=_l("Template type"))
    #admin.register(Channel, ChannelAdmin,
    #               category=_l("Content"), name=_l("Channel"))
    admin.register(
        Link,
        LinkAdmin,
        category=u"内容",
        name=u"链接"
    )
    admin.register(Config,
                   ConfigAdmin,
                   category=u"配置",
                   name=u"站点配置")
    admin.register(SubContentPurpose,
                   SubContentPurposeAdmin,
                   category=u"配置",
                   name=u"子内容用途")
    admin.register(ChannelType, ChannelTypeAdmin,
                   category=u"配置", name=u"频道类型")
    admin.register(ContentTemplateType,
                   ContentTemplateTypeAdmin,
                   category=u"配置",
                   name=u"模板类型")
    admin.register(Channel, ChannelAdmin,
                   category=u"内容", name=u"频道")

    # avoid registering twice
    if admin.app is None:
        admin.init_app(app)

    return admin
