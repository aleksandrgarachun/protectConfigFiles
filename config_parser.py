import yaml
from typing import Dict, Any
from config_schema import ConfigSchema  # Імпорт схеми

class ConfigParser:
    def __init__(self, config_file: str, schema: Dict[str, Any] = None):
        self.config_file = config_file
        self.schema = schema

    def parse(self) -> Dict[str, Any]:
        """
        Завантажує та парсить конфігураційний файл YAML, перевіряючи відповідність схемі.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)

            # Якщо задана схема, перевіряємо конфігурацію
            if self.schema:
                config_schema = ConfigSchema(self.schema)
                config_schema.validate(config)
                
            return config
        except (yaml.YAMLError, ValueError, TypeError) as e:
 
            return None
