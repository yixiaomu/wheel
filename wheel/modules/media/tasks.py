# coding=utf8
#

from __future__ import print_function
from wheel import create_celery_app

celery = create_celery_app()


@celery.task
def media_task():
    print("Doing something async...")  # noqa
