# coding=utf8
#


from flask.ext.mongoengine import MongoEngine
from .fields import ListField

db = MongoEngine()
db.ListField = ListField