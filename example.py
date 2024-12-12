from config_schema import ConfigSchema
from config_parser import ConfigParser

# Визначення схеми конфігурації
schema = {
    'database': {
        'host': str,
        'port': int,
        'username': str,
        'password': str
    },
    'debug': bool,
    'logfile': str
}

# Ініціалізація схеми
config_schema = ConfigSchema(schema)

# Парсинг конфігураційного файлу
config_parser = ConfigParser('config.yaml')
config = config_parser.parse()

# Валідація конфігурації згідно зі схемою
try:
    if config_schema.validate(config):
        print("Configuration is valid.")
except (ValueError, TypeError) as e:
    print(f"Configuration error: {e}")
