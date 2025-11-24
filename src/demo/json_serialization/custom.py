"""Generate metric in JSON"""
import json
from datetime import datetime

metric = {
    'time': datetime.now(),  # this field is cannot serialized by json library
    'name': 'memory',
    'value': 14.3,
    'labels': {
        'host': 'prod7',
        'version': '1.3.4',
    },
}


def pairs_hook(pairs):
    """Convert the "time" key to datetime"""
    obj = {}
    for key, value in pairs:
        if key == 'time':
            value = datetime.fromisoformat(value)  # Python >= 3.7
        obj[key] = value
    return obj


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


data = json.dumps(metric, default=default, indent=4)
print(data)

data = json.loads(data, object_hook=pairs_hook)
