import logging
import os
from pathlib import Path
from config.settings import load_settings


def setup_logging() -> logging.Logger:
    settings = load_settings()
    
    log_file_path = Path(settings.logging.file_path)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("luna")
    logger.setLevel(getattr(logging, settings.logging.level.upper()))
    
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()