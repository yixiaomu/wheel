#!/usr/bin/env python
# coding=utf8
#

from wheel.core.db import db
from wheel.core.models.content import Content


class Post(Content):
    # URL_NAMESPACE = 'wheel.modules.posts.detail'
    body = db.StringField(required=True)
