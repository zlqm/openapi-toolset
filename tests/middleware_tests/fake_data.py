import time


valid_pet_list = [
    {
        'id': 1,
        'name': 'Peter',
        'photos': [
            {
                'timestamp': int(time.time()),
                'url': 'http://',
                'description': 'hello'
            }
        ]
    }
]

invalid_pet_list = [
    {
        'name': 'Peter',
        'photos': [
            {
                'timestamp': int(time.time()),
                'url': 'http://',
                'description': 'hello'
            }
        ]
    }
]
