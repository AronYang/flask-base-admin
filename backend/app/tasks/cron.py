# coding=utf-8
import datetime

from app.tasks.test import hello


class Cron:

    @classmethod
    def hello(cls):
        hello()
