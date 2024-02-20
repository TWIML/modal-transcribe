import inspect
from backend import config

DEBUG = True

class DebugLogger:

    def __init__(self, logger):
        self.logger = logger

    def log(self, level='info', message=None):
        if not DEBUG:
            return
        
        if message is None:
            frame = inspect.stack()[2]
            func_name = frame[3]
            arg_info = inspect.getargvalues(frame[0])
            args = [f"{arg}={arg_info.locals[arg]}" for arg in arg_info.args]
            message = f"*** Entering function: {func_name}, args: {', '.join(args)} ***"

        if level == 'info':
            self.logger.info(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)

    def __call__(self, level='info', message=None):
        self.log(level, message)

logger = config.get_logger(__name__)
debug_logger = DebugLogger(logger)