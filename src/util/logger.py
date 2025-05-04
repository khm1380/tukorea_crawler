import logging


def configure_logging(level: int = logging.INFO) -> None:
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    logging.basicConfig(level=level, format=fmt)
