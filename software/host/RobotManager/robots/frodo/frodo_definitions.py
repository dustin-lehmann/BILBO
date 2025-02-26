import enum

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
        'front': 10,
        'back': 11
    },
    'static1': {
        'type': 'static',
        'front': 0,
        'back': 1
    }
}


def get_frodo_from_marker(marker_id) -> (str, float):
    ...