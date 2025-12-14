import logging


def init_logging(level=logging.INFO):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )


def switch_to_debug():
    logging.getLogger().setLevel(logging.DEBUG)
