# coding: utf-8
class QuestPeriod:
    ONCE = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


QUEST_PERIOD_CHOICES = (
    (QuestPeriod.ONCE, '单次任务'),
    (QuestPeriod.DAILY, '日常任务'),
    (QuestPeriod.WEEKLY, '每周任务'),
    (QuestPeriod.MONTHLY, '每月任务'),
)


class QuestRecordStatus:
    PENDING = 0
    ONGOING = 1
    # can get rewards
    REACH_CONDITIONS = 2
    # has get rewards
    COMPLETED = 3


QUEST_RECORD_STATUS_CHOICES = (
    (QuestRecordStatus.PENDING, '准备中'),
    (QuestRecordStatus.ONGOING, '正在进行中'),
    (QuestRecordStatus.REACH_CONDITIONS, '满足条件'),
    (QuestRecordStatus.COMPLETED, '已完成'),
)
