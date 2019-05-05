import os
import pkg.testbase.stcsession as stcsession
import pkg.testbase.snesession as snesession
import pkg.testbase.spirent_logger as spirent_logger
from pkg.testbase.settings import *

from genie.conf import Genie

# Genie extensions
import pkg.genie.libs.conf.device
import pkg.genie.libs.conf.device.iosxe.device

class TestBase():

    """
    Base class for test scripts.

    """
    def __init__(self, test_input):
        if not test_input or not test_input.outdir:
            raise RuntimeError("Must specify output directory")

        if not test_input.testbed:
            raise RuntimeError("Must specify testbed filename")

        self.stc = None
        self.sne = None
        self.logger = None
        self.test_input = test_input

    def setup(self):
        self.logger = spirent_logger.Logger(self.test_input.script_module, self.test_input.outdir, self.test_input.testcase_id)

        tb_path = os.path.join(self.test_input.outdir, self.test_input.testbed)
        if not os.path.exists(self.test_input.outdir) or not os.path.exists(tb_path):
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
            self.stc.download_all_files(self.test_input.outdir)
            self.stc.end()

        if self.sne is not None:
            self.sne.end()

        if self.logger is not None:
            self.logger.shutdown()
