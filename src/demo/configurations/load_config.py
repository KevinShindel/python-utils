"""Load configuration with exec"""
from types import SimpleNamespace


def load_config(path):
    """"Load configuration from path"""
    with open(path) as fp:
        data = fp.read()

    ns = {}
    exec(data, {}, ns)
    return SimpleNamespace(**ns)

if __name__ == '__main__':
    config = load_config('config.py')

    # print(config)
    print(config.DB_USER)
    print(config.DB_HOST)