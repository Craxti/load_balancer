import yaml
import json
import os


class Configuration:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.config = {}
        self.last_modified = 0

    def load(self):
        file_extension = self.get_file_extension()
        with open(self.config_file, 'r') as file:
            if file_extension == 'yaml':
                self.config = yaml.safe_load(file)
            elif file_extension == 'json':
                self.config = json.load(file)
            else:
                raise ValueError("Unsupported configuration file format")

        self.validate_config()
        self.last_modified = os.path.getmtime(self.config_file)

    def save(self):
        file_extension = self.get_file_extension()
        with open(self.config_file, 'w') as file:
            if file_extension == 'yaml':
                yaml.safe_dump(self.config, file)
            elif file_extension == 'json':
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
