import getpass
import os
import sys
import subprocess
import xml.dom.minidom as xmldom

from genie.conf import Genie
from pkg.testbase.settings import *

class SneDevice():

    """
    SNE Session using Genie
    """

    def __init__(self, sne_device, logger):
        """Initialize StcClient instance from testbed data."""
        self._logger = logger
        self._mapguid =  None
        self._name_port_map = {}
        self._chassis = None 

        if not sne_device or sne_device.type != SNE_TYPE:
            raise RuntimeError("Missing sne device")

        self._logger.info("===> Initializing new sne device" )
        ifaces = sne_device.interfaces
        for name, iface in ifaces.items():
            parsed_iface = iface.parse_interface_name()
            self._name_port_map[iface.alias] = parsed_iface.port

        self._chassis = str(sne_device.connections.chassis.ip)

    def configure(self):
        #Configure command
        command = SNE_CLI_CONFIGURE + 'ip '  + self._chassis + ' user ' + SNE_USER_NAME
        self._logger.info("===> configure SNE  %s" % (command))
        subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    
    def upload(self, config_file=None):
        #Sne does not supprot the ports relocatoin., so need replace the port number of sne configuration file
        if config_file == None:
            config = SNE_CONFIG_FILE;
        else:
            config = config_file

        self._reallocate_ports(config)

        self._logger.info("===> Uploading SNE configuraiton%s on %s" % (config, self._chassis))
        command = SNE_CLI_UPLOAD + config 
        p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out,err = p.communicate(timeout=SNE_CLI_COMMAND_TIMEOUT)
        out_info = out.decode('unicode-escape')
        lines = out_info.strip().split('\n')

        for line in lines:
            if line.find('mapguid') != -1 :
                info = line.split(':')
                if len(info) > 1:
                    self._mapguid = info[1]

        if self._mapguid is None:
            raise RuntimeError("Cannot get _mapguid")

    def stop(self):
        #Stop command
        if self._mapguid is not None:
            command = SNE_CLI_STOP + self._mapguid
            self._logger.info("===> SNE Stop command %s" % (command))
            self._executeCommand(command)
            self._mapguid = None

    def start(self):
        #Start command
        if self._mapguid is not None:
            command = SNE_CLI_START + self._mapguid
            self._logger.info("===> SNE start command %s" % (command))
            self._executeCommand(command)

    def enableObject(self, object_name):
        #Enable command: example: sne-cli F16344D3-35C8-4CDE-B1AC-88E3CF7AA05D DropPackets enabled true
        if self._mapguid is not None:
            command = SNE_CLI_SETPARAM + self._mapguid + ' ' + str(object_name) + ' enabled true'
            self._logger.info("===> SNE enableObject command %s" % (command))
            self._executeCommand(command)

    def disableObject(self, object_name):
        #Disable command: example: sne-cli F16344D3-35C8-4CDE-B1AC-88E3CF7AA05D DropPackets enabled false
        if self._mapguid is not None: 
            command = SNE_CLI_SETPARAM + self._mapguid + ' ' + str(object_name) + ' enabled false'
            self._logger.info("===> SNE disableObject command %s" % (command))
            self._executeCommand(command)

    def setparam(self, object_name, impairment_name, value):
        #e.g. cli setparam F16344D3-35C8-4CDE-B1AC-88E3CF7AA05D Delay1 delay 50
        if self._mapguid is not None:
            command = SNE_CLI_SETPARAM + self._mapguid + ' ' + str(object_name) + ' ' + str(impairment_name) + ' ' + str(value) 
            self._logger.info("===> SNE setparam command %s" % (command))
            self._executeCommand(command)

    def _reallocate_ports(self, config):
        #Reallocate the port number in the configuration file
        writeFile = False
        domobj = xmldom.parse(config)
        elementobj = domobj.documentElement
        subElementObj = elementobj.getElementsByTagName("Objects")
        if len(subElementObj) > 0:
            object_count = subElementObj[0].getAttribute("Count")
            for i in range(1, int(object_count)+1):
               subObjectElement = elementobj.getElementsByTagName("Object" + str(i))
               name = subObjectElement[0].getAttribute("Name")
               
               if name in self._name_port_map.keys():
                   item = subObjectElement.item(0)
                   portItem = item.getElementsByTagName('Port')
                   if (len(portItem) > 0) and (portItem[0].firstChild.data != self._name_port_map[name]):
                       portItem[0].firstChild.data = self._name_port_map[name]
                       writeFile = True
        if writeFile:
            try:
                f = open(config,'w',encoding='UTF-8')
                elementobj.writexml(f)
                f.close()
            except:
                raise RuntimeError("Cannot open file")

    def _executeCommand(self,command):
        result=False
        p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out,err = p.communicate(timeout=SNE_CLI_COMMAND_TIMEOUT)
        out_info = out.decode('unicode-escape')
        lines = out_info.strip().split('\n')
        for line in lines:
            if line.find('success') != -1 :
                result = True
                     
        if result==False: 
            raise RuntimeError("Commnand executed failed command=%s, out=%s, err=%s" % (command,out_info, err))
