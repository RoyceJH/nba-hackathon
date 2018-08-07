from constants import FREE_THROW, FREE_THROW_TECHNICAL, SHOT_ATTEMPT, FOUL, MADE_SHOT


def is_foul(event):
    return FOUL in event


def is_delayed_sub_over(event):
    return SHOT_ATTEMPT in event


def is_scoring_play(event, action):
    return MADE_SHOT in event or FREE_THROW_TECHNICAL in action or FREE_THROW in event


def lookup_event(event_code, play):
    event = event_code.loc[
        (event_code['"Event_Msg_Type"'] == play['Event_Msg_Type']) & (
                    event_code['"Action_Type"'] == play['Action_Type'])
        ]
    return event.values.flatten()
