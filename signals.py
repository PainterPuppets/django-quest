from django.dispatch import Signal

quest_change_status_signal = Signal(providing_args=["quest"])
quest_reach_conditions_signal = Signal(providing_args=["quest"])
quest_complete_signal = Signal(providing_args=["quest"])
