# coding: utf-8

from __future__ import print_function
from wheel import create_celery_app

celery = create_celery_app()


@celery.task
def comment_task():
    print("Doing something async...")  # noqa
