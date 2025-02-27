EMPTY_DATA = {
    'frodo1' : {
        'optitrack': {
            'valid': True,
            'position': [0.0, 1.0],
            'psi': 2.0
        },
        'agent': {
            'valid': True,
            'position': [3.0, 4.0],
            'psi': 5.0,
            'uncertainty': 6.0
        },
        'measurement': {
            'frodo1': {
                'visible': False,
                'tvec': [7.0, 8.0],
                'psi': 9.0,
                'tvec_uncertainty': 10.0,
                'psi_uncertainty': 11.0
            },
            'frodo2': {
                'visible': False,
                'tvec': [12.0, 13.0],
                'psi': 14.0,
                'tvec_uncertainty': 15.0,
                'psi_uncertainty': 16.0
            },
            'frodo3': {
                'visible': True,
                'tvec': [17.0, 18.0],
                'psi': 19.0,
                'tvec_uncertainty': 20.0,
                'psi_uncertainty': 21.0
            },
            'frodo4': {
                'visible': False,
                'tvec': [22.0, 23.0],
                'psi': 24.0,
                'tvec_uncertainty': 25.0,
                'psi_uncertainty': 26.0
            },
            'static1': {
                'visible': True,
                'tvec': [27.0, 28.0],
                'psi': 29.0,
                'tvec_uncertainty': 30.0,
                'psi_uncertainty': 31.0
            },
        }
    },
    'frodo2': {
        'optitrack': {
            ...
        }, 
        ...
    },
    'frodo3': {
        ...
    },
    'frodo4': {
        ...
    },
    'static1': {
        'optitrack': {
            'valid': True,
            'position': [0.0, 1.0],
            'psi': 2.0
        }
    }
}