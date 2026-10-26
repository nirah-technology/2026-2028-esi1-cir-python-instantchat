from dataclasses import dataclass
from pathlib import Path
from json import load

@dataclass
class ApplicationConfiguration:
    bind_address: str = "127.0.0.1"
    listen_port: int = 6666

    @staticmethod
    def load_configuration(configuration_file_path: Path = Path("config.json")):
        with open(configuration_file_path, 'r') as file_stream:
            content = load(file_stream)
        address = content.get("bind_address", "127.0.0.1")
        port = content["listen_port"]
        configuration = ApplicationConfiguration(
            bind_address=address,
            listen_port=port
        )
        return configuration
