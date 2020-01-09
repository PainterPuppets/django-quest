# coding: utf-8
from django.db import models
from jsonfield import JSONField


class Condition(models.Model):
    description = models.TextField()
    unique_name = models.CharField(max_length=255)
    extra_data = JSONField(default={}, blank=True, null=True)

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.__unicode__()
