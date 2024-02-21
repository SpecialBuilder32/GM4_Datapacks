from beet import Context
import logging
import re

def beet_default(ctx: Context):
    """Sets up a logging handler to repeat build log entries with the github action annotation format"""
    beet_logger = logging.getLogger(None) # get root logger

    handler = logging.StreamHandler()
    handler.setFormatter(AnnotationFormatter())

    beet_logger.addHandler(handler)

LEVEL_CONVERSION = {
    logging.DEBUG: "debug",
    logging.INFO: "notice",
    logging.WARNING: "warn",
    logging.ERROR: "error",
    logging.CRITICAL: "error"
}

class AnnotationFormatter(logging.Formatter):
    
    def format(self, record: logging.LogRecord) -> str:
        expl = record.message.split("\n")[0]

        filename = None
        line = None
        col = None
        match = re.match(r"(.+):(\d+):(\d+)", getattr(record, "annotate", ""))
        if match:
            filename, line, col = match.groups()

        level = LEVEL_CONVERSION.get(record.levelno, logging.INFO)
        return f"::{level} file={filename},line={line},col={col}::{expl}"
