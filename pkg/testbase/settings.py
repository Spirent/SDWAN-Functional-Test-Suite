import os
import sys

SPIRENT_OS = 'spirent'
SNE_TYPE = 'sne'
STC_TYPE = 'stc'
SNE_USER_NAME = 'testpack'
SNE_CONFIG_FILE = sys.path[0] + '/sneConfig.xml'
SNE_CLI = os.getcwd() + '/pkg/testbase/sne-cli'
SNE_CLI_UPLOAD = SNE_CLI + ' upload '
SNE_CLI_CONFIGURE = SNE_CLI + ' configure '
SNE_CLI_STOP = SNE_CLI + ' stop '
SNE_CLI_START = SNE_CLI + ' start '
SNE_CLI_SETPARAM = SNE_CLI + ' setparam '
SNE_CLI_COMMAND_TIMEOUT = 120
STC_DEVICE_CREATE_ARGS=['Port', 'IfCount', 'IfStack', 'DeviceCount','LoopbackIf', 'DeviceType','DeviceTags','DeviceRole','CreateCount','AffiliatedDevice']
STC_DEVICE_CONFIG_ARGS=['Name','EnablePingResponse','RouterId','RouterIdStep','Ipv6RouterId','Ipv6RouterIdStep']
STC_IF_NAME=['Ipv4If','Ipv6If','VlanIf','EthIIIf']
