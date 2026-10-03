import os
from logging import getLogger, StreamHandler, FileHandler, Formatter

_FORMATTER = Formatter(
    fmt="{asctime} - {levelname} - {filename}:{lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class Logger:
    def __init__(self) -> None:
        pass

    @staticmethod
    def log(name):
        
        logger = getLogger(name)

        stream_handler = StreamHandler()
        # 2. FileHandler can now safely open/create app.log inside the existing logs/ folder
        file_handler = FileHandler("logs/app.log", mode="a", encoding='utf-8')

        stream_handler.setFormatter(_FORMATTER)
        file_handler.setFormatter(_FORMATTER)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        logger.setLevel(level="DEBUG")

        return logger