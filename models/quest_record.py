# coding: utf-8
from django.db import models
from quests.models import Quest
from quests.constants import (
    QuestRecordStatus,
    QUEST_RECORD_STATUS_CHOICES,
    QuestPeriod,
)
from quests.utils import get_first_day_of_month_min_time, get_first_day_of_week_min_time, get_today_min_time


class QuestRecord(models.Model):
    recipient_id = models.CharField()
    quest = models.ForeignKey(Quest, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=QUEST_RECORD_STATUS_CHOICES,
        default=QuestRecordStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)

    @property
    def done(self):
        if self.status != QuestRecordStatus.COMPLETED:
            return False

        if not self.quest.is_periodic:
            return True

        if self.quest.period == QuestPeriod.DAILY:
            return self.created_at >= get_today_min_time()

        if self.quest.period == QuestPeriod.WEEKLY:
            return self.created_at >= get_first_day_of_week_min_time()

        if self.quest.period == QuestPeriod.MONTHLY:
            return self.created_at >= get_first_day_of_month_min_time()

        return False
