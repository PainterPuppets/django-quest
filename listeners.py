# coding: utf8
from quests.constants import QuestRecordStatus
from quests.services import QuestServices
from quests.signals import quest_change_status_signal, quest_reach_conditions_signal


def publish_condition_event(sender, instance, created, **kwargs):
    if not created:
        return

    recipient_id = instance.recipient_id
    quests = QuestServices.get_recipient_quest_list(recipient_id)

    pre_check_quests = []
    for quest in quests:
        if quest.conditions.filter(unique_name__contains=instance.unique_name).exists():
            pre_check_quests.append(quest)

    for quest in pre_check_quests:
        quest_status, can_be_completed = QuestServices.get_quest_status(recipient_id, quest)
        if not can_be_completed:
            quest_change_status_signal.send(sender=None, quest=quest)
            continue

        record = QuestServices.get_quest_available_record(recipient_id, quest)
        if record.status in [QuestRecordStatus.REACH_CONDITIONS, QuestRecordStatus.COMPLETED]:
            continue

        record.status = QuestRecordStatus.REACH_CONDITIONS
        record.save()
        quest_reach_conditions_signal.send(sender=None, quest=quest)
