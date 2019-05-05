'''
Device class for devices with junos OS.
'''

__all__ = (
    'Device',
)

from enum import Enum
import logging
import re
import telnetlib

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import genie.libs.conf.device
import genie.libs.conf.device.cisco

logger = logging.getLogger(__name__)


class Device(genie.libs.conf.device.cisco.Device):
    '''Device class for devices with junos OS'''

    logfile_messages_level = managedattribute(
        name='logfile_messages_level',
        default=5,
        type=(None, managedattribute.test_istype(int)))

    def connect(dut):
        host = str(dut.connections['a'].ip)
        tn = telnetlib.Telnet(host)
        tn.read_until(b"login: ", timeout=60)
        _tn_writeln(tn, dut.tacacs['username'])
        tn.read_until(b"Password: ", timeout=60)
        _tn_writeln(tn, dut.passwords['tacacs']
        dut.custom['handle'] = tn

    def config(dut):
        tn = dut.custom['handle']
        _tn_writeln(tn, "configure")

        for intf in dut.interfaces.values():
            w = ''.join(["set interface ", intf.type, " unit 0 family inet address ", str(intf.ipv4)])
            _tn_writeln(tn, w)

        _tn_writeln(tn, "commit")

    def disconnect(dut):
        tn = dut.custom['handle']
        _tn_writeln(tn, "exit")

def _tn_writeln(tn, w):
    tn.write(w.encode('ascii') + b"\n")
