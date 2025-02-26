import enum
import math

frodo_ids = ['frodo1', 'frodo2', 'frodo3', 'frodo4']
FRODO_USER_NAME = 'admin'
FRODO_PASSWORD = 'beutlin'

frodo_colors = {
    'frodo1': [72/255, 152/255, 2/255],
    'frodo2': [13/255, 166/255, 155/255],
    'frodo3': [166/255, 13/255, 13/255],
    'frodo4': [100/255, 13/255, 166/255]
}


markers = {
    'frodo1': {
        'type': 'robot',
        'front': 12,
        'back': 13
    },
    'frodo2': {
        'type': 'robot',
        'front': 14,
        'back': 15
    },
    'static1': {
        'type': 'static',
        'front': 0,
        'back': 1
    }
}


def get_title_from_marker(marker_id) -> (str, float):
    for key, marker in markers.items():
        if marker['front'] == marker_id:
            return key, 0.0
        elif marker['back'] == marker_id:
            return key, math.pi
        
    return None, 0.0