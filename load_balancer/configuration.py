import yaml
import json
import os
import dotenv


class Configuration:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.config = {}
        self.last_modified = 0

    def load(self):
        file_extension = self.get_file_extension()

        if file_extension == 'yaml':
            self.load_from_yaml()
        elif file_extension == 'json':
            self.load_from_json()
        else:
            raise ValueError("Unsupported configuration file format")

        self.validate_config()
        self.last_modified = os.path.getmtime(self.config_file)

    def load_from_yaml(self):
        with open(self.config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def load_from_json(self):
        with open(self.config_file, 'r') as file:
            self.config = json.load(file)

    def save(self):
        file_extension = self.get_file_extension()
        if file_extension == 'yaml':
            with open(self.config_file, 'w') as file:
                yaml.safe_dump(self.config, file)
        elif file_extension == 'json':
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file)
        else:
            raise ValueError("Unsupported configuration file format")

    def validate_config(self):
        # Implement configuration validation to ensure correctness and data integrity
        pass

    def reload(self):
        # Reload the configuration without restarting the application
        modified_time = os.path.getmtime(self.config_file)
        if modified_time > self.last_modified:
            self.load()

    def get(self, key):
        return self.config.get(key)

    def get_file_extension(self):
        return self.config_file.rsplit('.', 1)[-1]

    def load_from_environment_variables(self, prefix=''):
        dotenv.load_dotenv()
        for key, value in os.environ.items():
            if key.startswith(prefix):
                key = key[len(prefix):].lower().replace('_', '.')
                self.config[key] = value
