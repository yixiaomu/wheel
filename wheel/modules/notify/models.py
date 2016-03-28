# coding=utf8
#


import logging
import datetime
from wheel.core.db import db

logger = logging.getLogger()


class Notify(db.Document):
    type = db.StringField(choices=(('login', u'login'),
                                   ('comments', u'comments')))
    content = db.StringField()
    status = db.StringField(default='unread')   # unread, readed
    create_on = db.DateTimeField(default=datetime.datetime.now)
    modify_on = db.DateTimeField(default=datetime.datetime.now)