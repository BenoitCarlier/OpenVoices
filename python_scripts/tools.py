import re

pattern_name = '(?P<modality>\d{2})-(?P<vocal_channel>\d{2})-(?P<emotion>\d{2})-(?P<emotional_intensity>\d{2})-(?P<statement>\d{2})-(?P<repetition>\d{2})-(?P<actor>\d{2})\.wav'
regex_name = re.compile(pattern_name)

MAP_EMOTION = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'

}


def get_emotion(name):
    m = regex_name.search(name)
    if not m:
        raise Exception

    return MAP_EMOTION[str(m.group('emotion'))]
