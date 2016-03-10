# coding=utf8
#


from wheel import admin
from wheel.core.admin.models import ModelAdmin
from wheel.core.widgets import TextEditor
from wheel.modules.comments.models import Comment
from wheel.utils.translation import _l


class CommentAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'moderator')
    column_list = ('path', 'author_name', 'author_email',
                   'created_at', 'published')
    form_columns = ['path', 'author_email', 'author_name',
                    'content_format', 'body', 'replies',
                    'created_at', 'created_by', 'published']
    form_args = {
        'body': {'widget': TextEditor()}
    }


admin.register(Comment, CommentAdmin, category=_l('Content'),
               name=_l("Comments"))
