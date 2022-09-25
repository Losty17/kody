from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter, StreamHandler, getLogger


class CustomFormatter(Formatter):
    """ Custom logger formatting """

    grey = "\033[30m"
    cyan = "\033[36m"
    green = "\033[32m"
    purple = "\033[0;95m"
    bold_red = "\x1b[31;1m"
    bold_red_bg = "\x1b[0;101m"
    reset = "\x1b[0m"

    FORMATS = {
        DEBUG: grey,
        INFO: cyan,
        WARNING: purple,
        ERROR: bold_red,
        CRITICAL: bold_red_bg
    }

    def text(self, color):
        return f"{self.grey}%(asctime)s {self.green}[%(name)s] {color}%(levelname)s{self.reset} %(message)s"

    def format(self, record):
        return Formatter(
            self.text(self.FORMATS.get(record.levelno)),
            "%d/%m %H:%M:%S"
        ).format(record)


def setup_logger():
    ch = StreamHandler()
    ch.setLevel(DEBUG)

    ch.setFormatter(CustomFormatter())

    discord_logger = getLogger("discord")
    discord_logger.setLevel(INFO)
    getLogger("discord.gateway").setLevel(CRITICAL)

    logger = getLogger("kody")
    logger.setLevel(DEBUG)

    logger.addHandler(ch)
    discord_logger.addHandler(ch)

    return logger
