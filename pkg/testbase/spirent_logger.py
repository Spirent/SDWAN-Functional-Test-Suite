import json
import logging
import os
from datetime import datetime, timezone

class Logger(logging.LoggerAdapter):

    """
    Logger adapter class for Testpack test scripts. Produces structured logs adhering to
    JSON schema recommended by STC evolution project.

    """

    def __init__(self, module_name, test_out_dir, testcase_id):
        fh = logging.FileHandler(os.path.join(test_out_dir, 'test.log.json'), mode='w')
        fh.setFormatter(logging.Formatter('%(message)s'))
        logr = logging.getLogger(module_name)
        logr.addHandler(fh)
        super().__init__(logr, {'testcase_id': testcase_id})

    def shutdown(self):
        logging.shutdown()

    def debug(self, msg):
        if super().isEnabledFor(logging.DEBUG):
            super().debug(self.logMessage(msg, 'DEBUG'))

    def info(self, msg):
        if super().isEnabledFor(logging.INFO):
            super().info(self.logMessage(msg, 'INFO'))

    def warning(self, msg):
        super().warning(self.logMessage(msg, 'WARN'))

    def error(self, msg):
        super().error(self.logMessage(msg, 'ERROR'))

    def critical(self, msg):
        super().critical(self.logMessage(msg, 'FATAL'))

    def exception(self, msg):
        super().exception(self.logMessage(msg, 'ERROR'))

    def logMessage(self, msg, level):
        logrec = LogEntry(self.extra['testcase_id'], level, msg)
        return json.dumps(logrec.__dict__, default=str)

class LogEntry:

    def __init__(self, testcase_id, level, msg):
        self.logger = testcase_id
        self.level = level
        self.timestamp = datetime.now(timezone.utc)
        self.message = msg
