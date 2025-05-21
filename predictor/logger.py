import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from predictor.config import Config

_logger: Optional[logging.Logger] = None


def get_logger(
    name: str = "enviro_sentinel", config: Optional["Config"] = None
) -> logging.Logger:
    global _logger
    if _logger:
        return _logger

    if config is None:
        from predictor.config import load_config

        config = load_config()

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    print(config.LOG_LEVEL)
    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    formatter = logging.Formatter(config.LOG_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if config.LOG_FILE:
        log_path = Path(config.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    _logger = logger
    return logger
