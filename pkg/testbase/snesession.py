import getpass
import os
import sys
import subprocess
import xml.dom.minidom as xmldom

from genie.conf import Genie
import pkg.testbase.snedevice as snedevice

class SneSession():

    """
    SNE Session using Genie
    """

    def __init__(self, sne_devices, logger):
        """Initialize StcClient instance from testbed data."""
        self._logger = logger
        self.devices = {}

        if len(sne_devices) == 0:
            raise RuntimeError("Missing sne device")

        for sne_device in sne_devices:
            self._logger.info("===> Adding new sne device: %s" % (sne_device.name))
            self.devices[sne_device.name] = snedevice.SneDevice(sne_device, self._logger)

    def end(self):
        self._logger.info("===> SNE sessoin end")
        for name in self.devices:
            self.devices[name].stop()
