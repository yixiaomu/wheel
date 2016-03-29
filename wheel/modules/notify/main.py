# coding=utf8
#


from wheel.core.app import WheelModule
from .views import NotifyEditView


module = WheelModule('notify', __name__, template_folder='templates')
module.add_url_rule('/msg/notify/list/',
                    view_func=NotifyEditView.as_view('notify_list'))
