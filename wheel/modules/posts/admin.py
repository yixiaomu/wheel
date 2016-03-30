# coding=utf8
#


from wheel import admin
from wheel.core.admin.models import BaseContentAdmin
from wheel.core.widgets import TextEditor
from wheel.core.widgets import PrepopulatedText
from wheel.modules.posts.models import Post
from wheel.utils.translation import _l


class PostAdmin(BaseContentAdmin):

    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'content_format', 'body', 'authors', 'source',
                    'comments_enabled', 'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type', 'license']

    form_args = {
        'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }


#admin.register(Post, PostAdmin, category=_l("Content"), name=_l("Post"))
admin.register(Post, PostAdmin, category=u"内容", name=u"帖子")
