import logging


def init_logging(level: int = logging.DEBUG) -> None:
    """
    Initialisiert das Logging mit dem angegebenen Level und einem festen Format.
    Logdatei: app.log (wird überschrieben bei jedem Start).
    :param level: Logging-Level (z.B. logging.DEBUG, logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        filename="app.log",
        filemode="w",
    )


def switch_to_info() -> None:
    """
    Setzt das Logging-Level zur Laufzeit auf INFO.
    """
    logging.getLogger().setLevel(logging.INFO)