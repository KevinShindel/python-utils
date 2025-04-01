"""Generate metric in YAML & TOML"""
import toml
import yaml

metric = {
    'time': datetime.now(),
    'name': 'memory',
    'value': 14.3,
    'labels': {
        'host': 'prod7',
        'version': '1.3.4',
    },
}


print('YAML')
print(yaml.dump(metric, default_flow_style=False, sort_keys=False))

print('\nTOML')
print(toml.dumps(metric))

# de-serialize
with open('config.yml') as fp:
    config = yaml.safe_load(fp)
print(config)

# serialize
yaml.safe_dump(config, stdout)
