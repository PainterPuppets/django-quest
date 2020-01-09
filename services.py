from django.utils import timezone
from django.db.models import Q
from quests.models import ConditionEvent, Condition, QuestRecord, Quest
from quests.exceptions import QuestAlreadyCompletedException
from quests.signals import (
    quest_change_status_signal,
    quest_reach_conditions_signal,
    quest_complete_signal,
)
from quests.constants import QuestRecordStatus, QuestPeriod, RewardType
from quests.utils import get_first_day_of_month_min_time, get_first_day_of_week_min_time, get_today_min_time


class QuestServices(object):

    @classmethod
    def publish_event(cls, unique_name, recipient_id, extra_data={}):
        ConditionEvent.objects.create(
            unique_name=unique_name,
            recipient_id=recipient_id,
            extra_data=extra_data
        )

    @classmethod
    def complete_quest(cls, recipient_id, quest):
        quest_record = cls.get_quest_available_record(
            recipient_id=recipient_id,
            quest=quest
        )

        if quest_record.status == QuestRecordStatus.COMPLETED:
            raise QuestAlreadyCompletedException

        quest_record.status = QuestRecordStatus.COMPLETED
        quest_record.save()
        quest_complete_signal.send(sender=None, quest=quest)

    @classmethod
    def get_quest_available_record(cls, recipient_id, quest):
        if not quest.is_periodic:
            quest_record = QuestRecord.objects.filter(recipient_id=recipient_id, quest=quest)
            if not quest_record.exists():
                return QuestRecord.objects.create(
                    recipient_id=recipient_id,
                    quest=quest,
                    status=QuestRecordStatus.ONGOING
                )

            return quest_record.first()

        time_limit = get_today_min_time()

        if quest.period == QuestPeriod.WEEKLY:
            time_limit = get_first_day_of_week_min_time()

        if quest.period == QuestPeriod.MONTHLY:
            time_limit = get_first_day_of_month_min_time()

        record = QuestRecord.objects.filter(recipient_id=recipient_id, quest=quest, created_at__gte=time_limit)
        if record.exists():
            return record.first()

        return QuestRecord.objects.create(recipient_id=recipient_id, quest=quest, status=QuestRecordStatus.ONGOING)

    @classmethod
    def get_recipient_quest_list(cls, recipient_id):
        records = QuestRecord.objects.filter(
            recipient_id=recipient_id
        )
        had_done_records = filter(lambda r: r.done, records)
        had_done_quest_ids = list(set(map(lambda r: r.quest_id, had_done_records)))

        quests = Quest.objects.filter(
            Q(start_at__isnull=True) |
            Q(start_at__lte=timezone.now()),
            Q(end_at__isnull=True) |
            Q(end_at__gte=timezone.now())
        )

        quests = quests.exclude(id__in=had_done_quest_ids)
        quests = quests.filter(
            Q(requirement__isnull=True) |
            Q(requirement__isnull=False, requirement__id__in=had_done_quest_ids)
        )

        return quests

    @classmethod
    def get_quest_status(cls, recipient_id, quest):
        def _check_key_match(key, value, obj):
            if key not in obj:
                return False
            if obj[key] != value:
                return False

            return True

        result = {}
        record = cls.get_quest_available_record(recipient_id, quest)
        if record.status in [QuestRecordStatus.COMPLETED, QuestRecordStatus.REACH_CONDITIONS]:
            conditions = quest.conditions.all()
            for condition in conditions:
                result[condition.unique_name] = {
                    'current': condition.count,
                    'requirement': condition.count,
                    'complete': True
                }

            return result, True

        conditions = quest.conditions.all()
        events = ConditionEvent.objects.filter(
            recipient_id=recipient_id
        )
        if quest.start_at:
            events = events.filter(created_at__gte=quest.start_at)

        if quest.end_at:
            events = events.filter(created_at__lte=quest.end_at)

        if quest.is_periodic:
            time_limit = get_today_min_time()

            if quest.period == QuestPeriod.WEEKLY:
                time_limit = get_first_day_of_week_min_time()

            if quest.period == QuestPeriod.MONTHLY:
                time_limit = get_first_day_of_month_min_time()
            events = events.filter(created_at__gte=time_limit)

        if not conditions.exists():
            return result, True

        can_be_completed = events.exists()
        for condition in conditions:
            eligible = list(events.filter(unique_name=condition.unique_name))

            for key in condition.extra_data.keys():
                eligible = list(filter(lambda e: _check_key_match(key, condition.extra_data[key], e.extra_data), eligible))

            result[condition.unique_name] = {
                'current': len(eligible),
                'requirement': condition.count,
                'complete': len(eligible) >= condition.count
            }

            if len(eligible) < condition.count:
                can_be_completed = False

        return result, can_be_completed
