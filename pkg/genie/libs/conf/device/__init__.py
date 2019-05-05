# Genie extension
import genie.libs.conf.device

def showlog(self):
    return NotImplemented

genie.libs.conf.device.Device.showlog = showlog
