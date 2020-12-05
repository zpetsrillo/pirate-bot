class BotLogger:
    def __init__(self, logger):
        self.logger = logger

    def log(self, s):
        print("INFO: " + s)
        self.logger.info(s)

    def warn(self, s):
        print("WARNING: " + s)
        self.logger.warn(s)

    def error(self, s):
        print("ERROR: " + s)
        self.logger.error(s)