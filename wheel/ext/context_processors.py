# coding=utf8
#


import datetime
from wheel.core.models.channel import Channel
from wheel.core.models.config import Config
from wheel.core.models.content import Link
from wheel.core.models.content import Content


def configure(app):

    @app.context_processor
    def inject():
        now = datetime.datetime.now()
        return dict(
            channels=Channel.objects(published=True,
                                     available_at__lte=now,
                                     parent=None),
            Config=Config,
            Content=Content,
            Channel=Channel,
            homepage=Channel.get_homepage(),
            Link=Link
        )
