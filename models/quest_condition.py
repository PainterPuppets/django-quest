# coding: utf-8
from quest.models import Condition, Quest
from django.db import models


class QuestCondition(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.PROTECT)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)
    count = models.IntegerField(default=1)
