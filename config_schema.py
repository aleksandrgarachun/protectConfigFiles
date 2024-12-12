from typing import Dict, Any

class ConfigSchema:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate(self, config: Dict[str, Any], schema: Dict[str, Any] = None) -> bool:
        """
        Рекурсивно перевіряє конфігурацію згідно зі схемою.
        """
        if schema is None:
            schema = self.schema
        for key, value in schema.items():
            if key not in config:
                raise ValueError(f"Missing key: {key}")
            if isinstance(value, dict):
                self.validate(config[key], value)
            else:
                if not isinstance(config[key], value):
                    raise TypeError(f"Incorrect type for key: {key}. Expected {value}, got {type(config[key])}")
        return True
