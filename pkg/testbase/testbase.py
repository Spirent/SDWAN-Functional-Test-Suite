import os
import pkg.testbase.stcsession as stcsession
import pkg.testbase.snesession as snesession
import pkg.testbase.spirent_logger as spirent_logger
from pkg.testbase.settings import *

from genie.conf import Genie

class TestBase():

    """
    Base class for test scripts.

    """
    def __init__(self, logger_name, output_dir, testbed_filename):
        if not output_dir:
            raise RuntimeError("Must specify output directory")

        if not testbed_filename:
            raise RuntimeError("Must specify testbed filename")

        self.stc = None
        self.sne = None
        self.logger = None
        self.outdir = output_dir

        self._logger_name = logger_name
        self._testbed_filename = testbed_filename

    def setup(self):
        tc_id = os.getenv(TESTCASE_ID_ENV, 'Unknown')
        self.logger = spirent_logger.Logger(self._logger_name, self.outdir, tc_id)

        tb_path = os.path.join(self.outdir, self._testbed_filename)
        if not os.path.exists(self.outdir) or not os.path.exists(tb_path):
            raise RuntimeError("no such file: " + tb_path)

        self.testbed = None
        try:
            self.testbed = Genie.init(tb_path)
        except Exception as e:
            raise e.__context__

        self.stc = stcsession.StcSession(self.testbed, self.logger, debug_level=1)
        self.stc.start()

        sne_devices = self.testbed.find_devices(os=SPIRENT_OS, type=SNE_TYPE)
        if len(sne_devices) > 0:
            self.sne = snesession.SneSession(sne_devices, self.logger)

    def cleanup(self):
        if self.stc is not None:
            self.stc.end()

        if self.sne is not None:
            self.sne.end()

        if self.logger is not None:
            self.logger.shutdown()
