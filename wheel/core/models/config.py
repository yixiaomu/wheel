#!/usr/bin/env python
# coding=utf8


import logging
from flask import current_app
from wheel.core.db import db
from wheel.core.fields import MultipleObjectsReturned
from wheel.core.models.custom_values import HasCustomValue
from wheel.core.models.signature import Dated
from wheel.core.models.signature import Slugged
from wheel.core.models.signature import Publishable
from wheel.core.models.signature import ContentFormat

logger = logging.getLogger()


class Config(HasCustomValue, ContentFormat, Publishable, db.DynamicDocument):
    group = db.StringField(max_length=255)
    description = db.StringField()

    @classmethod
    def get(cls, group, name=None, default=None):

        try:
            instance = cls.objects.get(group=group)
        except:
            return None

        if not name:
            ret = instance.values
            if group == 'settings':
                ret = {}
                ret.update(current_app.config)
                ret.update({item.name: item.value for item in instance.values})
        else:
            try:
                ret = instance.values.get(name=name).value
            except (MultipleObjectsReturned, AttributeError):
                ret = None

        if not ret and group == 'settings' and name is not None:
            # get direct from store to avoid infinite loop
            ret = current_app.config.store.get(name)

        return ret or default

    def __unicode__(self):
        return self.group


class Wheel(Dated, Slugged, db.DynamicDocument):
    """ Hidden collection for installation control"""
