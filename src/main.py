from __future__ import annotations

from pipeline.climate_pipeline import ClimatePipeline
from utils.logger import configure_logging, get_logger


def main() -> None:
    """Run the climate intelligence pipeline."""
    configure_logging()
    logger = get_logger(__name__)

    pipeline = ClimatePipeline()
    if not pipeline.run():
        logger.error("Climate pipeline finished with errors.")


if __name__ == "__main__":
    main()

