import ipaddress
import os
import time
import pkg.testbase.spirent_logger as spirent_logger
from pkg.testbase.testbase import TestBase
from snesession import SneSession

from genie.conf import Genie

#############################################################################
# Sample script to for SNE #
# There is no DUT and STC configuraion , just a sample how to use SneSession#
# TODO: Add a complete configuraion including STC and DUT
#############################################################################


class sne_sample(TestBase):

    def __init__(self):
        super().__init__(__name__)

    def setup(self, test_out_dir, testbed_file):
        super().setup(test_out_dir, testbed_file)

    def run(self):
        #...
        sne1 = self.sne.devices['sne']
        sne1.configure()
        sne1.upload()

        sne1.start()
        sne1.stop()
        #...
