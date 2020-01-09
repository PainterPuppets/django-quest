# coding: utf-8
from django.db import models
from quests.models import Condition
from quests.constants import (
    QuestPeriod,
    QUEST_PERIOD_CHOICES
)


class Quest(models.Model):
    is_valid = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    period = models.IntegerField(
        choices=QUEST_PERIOD_CHOICES,
        default=QuestPeriod.ONCE,
    )

    requirement = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    conditions = models.ManyToManyField(Condition, blank=True, through='QuestCondition')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    @property
    def is_periodic(self):
        return self.period != QuestPeriod.ONCE
