# coding=utf8
#


from flask import url_for
from flask.ext.admin import form
from jinja2 import Markup

from wheel import admin
from wheel.utils.settings import get_setting_value
from wheel.core.models.channel import Channel
from wheel.core.admin.models import ModelAdmin
from wheel.core.admin.fields import ImageUploadField
from wheel.utils.upload import dated_path
from wheel.utils.upload import lazy_media_path
from wheel.core.admin.models import BaseContentAdmin
from wheel.core.widgets import TextEditor
from wheel.core.widgets import PrepopulatedText
from wheel.core.admin.ajax import AjaxModelLoader
from wheel.utils.translation import _l

from wheel.modules.media.models import File
from wheel.modules.media.models import Image
from wheel.modules.media.models import Video
from wheel.modules.media.models import Audio
from wheel.modules.media.models import MediaGallery


class MediaAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_list = ('title', 'full_path', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'content_format',
                    'summary', 'comments_enabled', 'published']

    form_overrides = {
        'path': form.FileUploadField
    }

    form_args = {
        'summary': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')},
    }

    form_widget_args = {
        'channel': {'data-placeholder': _l('media/')}
    }


class FileAdmin(MediaAdmin):
    form_args = {
        'path': {
            'label': 'File',
            'base_path': lazy_media_path(),
            'namegen': dated_path,
            'permission': 0o777
        },
        'summary': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')},
    }

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/files"}
        )
    }


class VideoAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/video"}
        )
    }


class AudioAdmin(FileAdmin):
    form_columns = ['title', 'slug', 'path', 'embed',
                    'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/audio"}
        )
    }


class ImageAdmin(MediaAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_list = ('title', 'full_path', 'thumb', 'published')
    form_columns = ['title', 'slug', 'path', 'channel', 'content_format',
                    'comments_enabled', 'summary', 'published']

    @staticmethod
    def _list_thumbnail(context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s" width="100">' % url_for(
                'wheel.core.media',
                filename=form.thumbgen_filename(model.path)
            )
        )

    column_formatters = {
        'thumb': _list_thumbnail
    }

    form_extra_fields = {
        'path': ImageUploadField(
            'Image',
            base_path=lazy_media_path(),
            thumbnail_size=get_setting_value('MEDIA_IMAGE_THUMB_SIZE',
                                             default=(200, 200, True)),
            endpoint="wheel.core.media",
            namegen=dated_path,
            permission=0o777,
            allowed_extensions="MEDIA_IMAGE_ALLOWED_EXTENSIONS",
        )
    }

    form_ajax_refs = {
        'channel': AjaxModelLoader(
            'channel',
            Channel,
            fields=['title', 'slug', 'long_slug'],
            filters={"long_slug__startswith": "media/image"}
        )
    }


class MediaGalleryAdmin(BaseContentAdmin):
    roles_accepted = ('admin', 'editor', 'author')
    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'content_format', 'body',
                    'comments_enabled', 'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type']

    form_args = {
        'body': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }


#admin.register(File, FileAdmin, category=_l('Media'), name=_l("File"))
#admin.register(Video, VideoAdmin, category=_l('Media'), name=_l("Video"))
#admin.register(Audio, AudioAdmin, category=_l('Media'), name=_l("Audio"))
#admin.register(Image, ImageAdmin, category=_l('Media'), name=_l("Image"))
#admin.register(MediaGallery, MediaGalleryAdmin,
#               category=_l('Content'), name=_l("Media Gallery"))
admin.register(File, FileAdmin, category=u"多媒体", name=u"文件")
admin.register(Video, VideoAdmin, category=u'多媒体', name=u"视频")
admin.register(Audio, AudioAdmin, category=u'多媒体', name=u"音频")
admin.register(Image, ImageAdmin, category=u'多媒体', name=u"图片")
admin.register(MediaGallery, MediaGalleryAdmin,
               category=u'内容', name=u"图片相册")
