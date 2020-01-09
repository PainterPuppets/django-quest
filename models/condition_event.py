# coding: utf-8
from django.db import models
from django.db.models.signals import post_save
from jsonfield import JSONField
from quests.models import Condition
from quests.listeners import publish_condition_event


class ConditionEvent(models.Model):
    recipient_id = models.CharField()
    unique_name = models.CharField(max_length=255, default='')
    extra_data = JSONField(default={}, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return '%s' % self.__str__()

    def __str__(self):
        return 'Condition Event: %s' % self.unique_name


post_save.connect(publish_condition_event, sender=ConditionEvent)
