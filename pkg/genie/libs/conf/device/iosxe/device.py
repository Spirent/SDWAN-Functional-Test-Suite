# Genie extension
import genie.libs.conf.device.iosxe.device

def showlog(self):
    cmd = 'show version'
    out = self.execute(cmd)
    return out

genie.libs.conf.device.iosxe.device.Device.showlog = showlog
