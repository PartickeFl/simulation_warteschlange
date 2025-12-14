import logging


def init_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        filename="app.log",
        filemode="w",
    )


def switch_to_info():
    logging.getLogger().setLevel(logging.INFO)