from __future__ import annotations

import logging

from utils.config import PipelineConfig


def configure_logging() -> None:
    """Configure application-wide logging once."""
    PipelineConfig.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(PipelineConfig.PIPELINE_LOG_PATH, mode="a"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for a module."""
    return logging.getLogger(name)
