# coding=utf8
# 

"""
included all the notify messages
"""

import os
from werkzeug import secure_filename
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import current_app
from flask.views import MethodView
from wheel.utils import get_current_user
from wheel.utils.upload import lazy_media_path
from flask.ext.security.utils import url_for_security
from flask.ext.security import current_user
from flask.ext.mongoengine.wtf import model_form
from wheel.core.templates import render_template
from .models import Notify


class NotifyEditView(MethodView):
    """
    Show User Profile
    """

    form = model_form(
        Notify,
        only=[
            'type',
            'create_on',
            'modify_on',
            'status',
            'content',
        ]
    )

    def get(self, notify_id):
        return render_template('notify/list.html')
