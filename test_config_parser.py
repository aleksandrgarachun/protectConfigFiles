import unittest
import os
from config_parser import ConfigParser
import yaml

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config_file = 'test_config.yaml'
        self.schema = {
            'database': {
                'host': str,
                'port': int,
                'username': str,
                'password': str
            },
            'debug': bool,
            'logfile': str
        }
        with open(self.config_file, 'w') as file:
            file.write("""
database:
  host: "localhost"
  port: 5432
  username: "user"
  password: "pass"
debug: true
logfile: "/var/log/app.log"
""")

    def tearDown(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_parse(self):
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        expected_config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass"
            },
            'debug': True,
            'logfile': "/var/log/app.log"
        }
        self.assertEqual(config, expected_config)

    def test_empty_file(self):
        with open(self.config_file, 'w') as file:
            file.write("")
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        self.assertIsNone(config)  # Очікуємо None для порожнього файлу

    def test_missing_file(self):
        os.remove(self.config_file)
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        with self.assertRaises(FileNotFoundError):
            config_parser.parse()

    def test_invalid_yaml(self):
        with open(self.config_file, 'w') as file:
            file.write("""
database:
  host: "localhost"
  port: not_a_number
  username: "user"
  password: "pass"
""")  # некоректне значення `port`
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        self.assertIsNone(config)  # Очікуємо None для некоректного YAML

    def test_extra_keys(self):
        with open(self.config_file, 'w') as file:
            file.write("""
database:
  host: "localhost"
  port: 5432
  username: "user"
  password: "pass"
  extra_key: "extra_value"
debug: true
logfile: "/var/log/app.log"
extra_field: "extra"
""")
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        expected_config = {
            'database': {
                'host': "localhost",
                'port': 5432,
                'username': "user",
                'password': "pass",
                'extra_key': "extra_value"
            },
            'debug': True,
            'logfile': "/var/log/app.log",
            'extra_field': "extra"
        }
        self.assertEqual(config, expected_config)

    def test_correct_types(self):
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        self.assertIsInstance(config['database']['port'], int)
        self.assertIsInstance(config['debug'], bool)
        self.assertIsInstance(config['database']['host'], str)

    def test_invalid_key_type(self):
        with open(self.config_file, 'w') as file:
            file.write("""
database:
  host: "localhost"
  port: "not_a_number"  # некоректний тип
  username: "user"
  password: "pass"
debug: true
logfile: "/var/log/app.log"
""")
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        self.assertIsNone(config)  # Очікуємо None для некоректного типу

    def test_schema_missing_key(self):
        with open(self.config_file, 'w') as file:
            file.write("""
database:
  host: "localhost"
  username: "user"
  password: "pass"
debug: true
logfile: "/var/log/app.log"
""")  # Відсутній ключ `port`
        config_parser = ConfigParser(self.config_file, schema=self.schema)
        config = config_parser.parse()
        self.assertIsNone(config)  # Очікуємо None через відсутній ключ

if __name__ == '__main__':
    unittest.main()
