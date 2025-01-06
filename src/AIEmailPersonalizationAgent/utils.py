import yaml
from typing import Union
from box import ConfigBox
import os

def read_yaml_file(file_path:os.path, return_config_box:bool=True)-> Union[ConfigBox, dict]:
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        if return_config_box:
            return ConfigBox(data)
        else:
            return data
    except FileNotFoundError:
        raise



if __name__ == "__main__":
    __all__ = ["read_yaml_file"]