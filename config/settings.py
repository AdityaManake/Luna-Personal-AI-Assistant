import os
import yaml 
from pathlib import Path 
from pydantic import BaseModel 
from dotenv import load_dotenv

load_dotenv(override=True)

class ModeConfig(BaseModel):
    model: str
    context_size: int = 4096
    temperature: float = 0.7
    max_tokens: int = 2048
    keep_alive: str = "3m"

class ModelConfig(BaseModel):
    default_mode: str = "normal"
    modes: dict[str,ModeConfig]
    vision: dict = {}

class LoggingConfig(BaseModel):
    level : str = os.getenv("LOG_LEVEL", "INFO")
    file_path: str = os.path.join("logs", "luna.log")

class Settings(BaseModel):
    ollama_host: str = os.getenv("OLLAMA_HOST").strip()
    logging: LoggingConfig = LoggingConfig()
    models: ModelConfig



def load_settings(yaml_path: str = os.path.join("config", "model_config.yaml")) -> Settings:
    path = Path(yaml_path)
    with open(path, "r") as f:
        yaml_data = yaml.safe_load(f)

    return Settings(models = ModelConfig(**yaml_data))

if __name__ == "__main__":
    s = load_settings()
    print("Host:", s.ollama_host)
    print("Default Mode:", s.models.default_mode)
    print("Default Model:", s.models.modes[s.models.default_mode].model)
    print("Log Level:", s.logging.level)
    print("Log Path:", s.logging.file_path)
