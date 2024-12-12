import unittest
from config_schema import ConfigSchema

class TestConfigSchema(unittest.TestCase):

    def setUp(self):
        self.schema = {
            'database': {
                'host': str,
                'port': int,
                'username': str,
                'password': str
            },
            'debug': bool,
            'logfile': str,
            'application': {
                'name': str,
                'version': str,
                'settings': {
                    'debug': bool,
                    'timeout': int
                }
            }
        }
        self.config_schema = ConfigSchema(self.schema)

    def test_valid_config(self):
        config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'application': {
                'name': "Test App",
                'version': "1.0",
                'settings': {
                    'debug': True,
                    'timeout': 30
                }
            }
        }
        self.assertTrue(self.config_schema.validate(config))

    def test_missing_key(self):
        config = {
            'database': {
                'host': "localhost",
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log"
        }
        with self.assertRaises(ValueError):
            self.config_schema.validate(config)

    def test_incorrect_type(self):
        config = {
            'database': {
                'host': "localhost",
                'port': "5432",  # Неправильний тип
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'application': {
                'name': "Test App",
                'version': "1.0",
                'settings': {
                    'debug': True,
                    'timeout': 30
                }
            }
        }
        with self.assertRaises(TypeError):
            self.config_schema.validate(config)

    def test_extra_key(self):
        config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'extra_key': "extra_value",  # Додатковий ключ
            'application': {
                'name': "Test App",
                'version': "1.0",
                'settings': {
                    'debug': True,
                    'timeout': 30
                }
            }
        }
        self.assertTrue(self.config_schema.validate(config))  # Додаткові ключі не викликають помилок

    def test_partial_config(self):
        config = {
            'database': {
                'host': "localhost",
                'username': "user",
                'password': "pass"
            },
            'debug': True
        }
        with self.assertRaises(ValueError):
            self.config_schema.validate(config)

    def test_non_dict_config(self):
        config = ["not", "a", "dictionary"]  # Некоректний формат
        with self.assertRaises(ValueError):
            self.config_schema.validate(config)

    def test_deeply_nested_dict(self):
        config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'application': {
                'name': "Test App",
                'version': "1.0",
                'settings': {
                    'debug': True,
                    'timeout': 30,
                    'max_connections': 100  # Додатковий ключ у вкладеній конфігурації
                }
            }
        }
        self.assertTrue(self.config_schema.validate(config))

    def test_invalid_type_in_nested_dict(self):
        config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'application': {
                'name': "Test App",
                'version': "1.0",
                'settings': {
                    'debug': True,
                    'timeout': "not_a_number"  # Неправильний тип
                }
            }
        }
        with self.assertRaises(TypeError):
            self.config_schema.validate(config)

if __name__ == '__main__':
    unittest.main()
