# coding= utf -8


from wtforms.fields import TextField
from wtforms.widgets import PasswordInput
from wheel import admin
from wheel.core.admin.models import ModelAdmin
from wheel.utils.translation import _l

from .models import Role, User, Connection


class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_searchable_list = ('name', 'email')
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')
    form_columns = ('name', 'email', 'roles', 'active', 'newpassword',
                    'confirmed_at',
                    'last_login_at', 'current_login_at', 'last_login_ip',
                    'current_login_ip', 'login_count', 'tagline',
                    'gravatar_email', 'use_avatar_from',
                    'avatar_file_path', 'avatar_url',
                    'bio', 'links', 'values')

    form_extra_fields = {
        "newpassword": TextField(widget=PasswordInput())
    }

    def on_model_change(self, form, model, is_created):
        if model.newpassword:
            setpwd = model.newpassword
            del model.newpassword
            model.set_password(setpwd, save=True)


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description', 'values')


class ConnectionAdmin(ModelAdmin):
    roles_accepted = ('admin',)


admin.register(User, UserAdmin, category=u"帐号管理", name=u"用户管理")
admin.register(Role, RoleAdmin, category=u"帐号管理", name=u"权限管理")
admin.register(Connection, ConnectionAdmin, category=u"帐号管理", name=u"用户权限关系管理")
