import getpass
import os

from genie.conf import Genie
from pkg.testbase.settings import *
from stcrestclient import stchttp

LS_SERVER_TYPE = 'stc-lab-server'
STC_PORT_TYPE = 'stc-port'
DEFAULT_HTTP_TIMEOUT_SEC = 120

class StcSession():

    """
    Spirent TestCenter ReST Session from pyATS topology.

    """

    def __init__(self, testbed, logger, session_name="", user_name="", debug_level=0):
        """Initialize StcClient instance from testbed data."""

        self._logger = logger
        self._stc = None
        self._csp_port_map = {}
        self._name_port_map = {}

        self._logger.debug("Enter StcSession.init()")

        self._ls_addr = None
        for name, server in testbed.servers.items():
            if server.type == LS_SERVER_TYPE:
                self._ls_addr = server.address
                break

        if not self._ls_addr:
            raise RuntimeError("testbed missing lab server")

        stc_devices = testbed.find_devices(os=SPIRENT_OS, type=STC_TYPE)
        if len(stc_devices) == 0:
            raise RuntimeError("topology missing stc")

        for stc_device in stc_devices:
            ifaces = stc_device.interfaces
            for name, iface in ifaces.items():
                if iface.type != STC_PORT_TYPE:
                    continue

                c = iface.chassis
                parsed_iface = iface.parse_interface_name()
                csp = "//%s/%s/%s" % (c, parsed_iface.slot, parsed_iface.port)
                if csp in self._csp_port_map:
                    raise RuntimeError("duplicate ports %s" % csp)

                iface.location = csp
                iface.handle = None

                self._csp_port_map[csp] = iface
                self._name_port_map[stc_device.name] = iface

        if not session_name:
            session_name = testbed.name

        self._http_timeout = DEFAULT_HTTP_TIMEOUT_SEC
        self._user_name = user_name
        self._session_name = session_name
        self._dbg_level = debug_level

    def __getattr__(self, name):
        # Forward any attributes provided by stchttp.StcHttp
        if self._stc is None:
            raise RuntimeError("not started")
        return getattr(self._stc, name)

    def __str__(self):
        # String a line with csp + interface name for each port
        strs = []
        for csp, port in self._csp_port_map.items():
            strs.append("%s (%s)" % (csp, port.alias))

        strs.sort()
        return '\n'.join(strs)

    def start(self):
        """Start test session and connect to all STC ports in testbed

        The session that is created is named with the session name and the user
        name separated with ' - '.

        """
        self._logger.debug("Enter StcSession.start()")

        if self._stc is not None:
            raise RuntimeError("already started")

        # Connect to lab server
        stc = stchttp.StcHttp(self._ls_addr, timeout=self._http_timeout,
                              debug_print=bool(self._dbg_level > 1))

        # Create new test session
        user_name = self._user_name

        # If user name not specified, try to get the name of the current user.
        if not user_name:
            try:
                user_name = getpass.getuser()
            except:
                pass

        if self._dbg_level:
            self._logger.info("===> Starting new test session %s" % (self._session_name))

        stc.new_session(user_name, self._session_name, True)
        self._logger.info("Lab Server running STC version %s" % (stc.bll_version()))
        self._stc = stc

        try:
            # Create project
            self._project = stc.create('project')

            # Create and reserve all ports.
            stc_ports = []
            for port in self._name_port_map.values():
                csp = port.location
                if self._dbg_level:
                    self._logger.info("===> Creating port: %s" % (csp))
                port.handle = stc.create('port', self._project, location=csp)
                stc_ports.append(port.handle)

            # Connect, reserve and map ports
            if self._dbg_level:
                self._logger.info("===> Attaching ports: %s" % (stc_ports))
            stc.perform('AttachPorts', portList=stc_ports, autoConnect='TRUE')

        except Exception as e:
            self.end()
            raise

        if self._dbg_level:
            self._logger.info("===> Started session: %s" % (stc.session_id()))
            sys_info = stc.system_info()
            del sys_info['supported_api_versions']
            for k, v in sys_info.items():
                self._logger.info("%s: %s     " % (k, v))

    def end(self):
        """Release ports and terminate test session"""
        if self._stc is None:
            self._logger.info("===> STC session not started")
            return

        # Release all ports.
        for port in self._name_port_map.values():
            if not port.handle:
                continue
            csp = port.location
            if self._dbg_level:
                self._logger.info("===> releasing port: %s" % (csp))
            try:
                self._stc.perform('releasePort', location=csp)
            except Exception as e:
                self._logger.info("release port %s: %s" % (csp, e))
            del port.handle

        # Disconnect all chassis and end test session.
        if self._dbg_level:
            self._logger.info("===> disconnecting all chassis")
        try:
            self._stc.disconnectall()
        except Exception as e:
            self._logger.error("disconnect chassis: %s" % (str(e)))

        self._stc.end_session()
        if self._dbg_level:
            self._logger.info("===> ended session: %s" % (self._stc.session_id()))

        self._stc = None

    def ls_address(self):
        """Return the Lab Server address"""
        return self._ls_addr

    def ports(self):
        """Return a slice of port dicts"""
        return [port for port in self._name_port_map.values()]

    def port(self, name):
        """Lookup information for a port by its stc port number.

        If port is connected/reserved, then 'handle' key has a value.

        """
        return self._name_port_map.get(name)

    def sne_port(self, name):
        """Lookup information for a SNE port by its alias.

        """
        return self._sne_port_map.get(name)
    @staticmethod
    def split_csp(csp):
        """Split a port location (//c/s/p) into chassis, slot, and port.

        Slot and port are returned as ints.

        """
        c, s, p = csp.strip('/').split('/')
        return c, int(s), int(p)

    def started(self):
        """Return True is test session started"""
        return bool(self._stc)

    def project(self):
        """Return the STC project"""
        return self._project

    def download_all_files(self, test_out_dir):
        """Download STC files(BLL/IL Logs, configuration file...)"""
        if os.path.exists(test_out_dir):
            self._stc.perform('GetEquipmentLogsCommand', {'EquipmentList': self._project})
            self._logger.info("Downloading all STC files")
            self._stc.download_all(dst_dir=test_out_dir)
        else:
            raise Exception("Destination directory: %s is not existing" % test_out_dir)

    def device_config(self, **args):
        """ 
        Config device
        """
        device_create_args = {}
        device_config_args = {}
        stack_args = {}
        stack = False
        for key, value in args.items():
            if key in STC_DEVICE_CREATE_ARGS:
                device_create_args[key] = value 
                if key == 'IfStack':
                    stack = True
            elif key in STC_DEVICE_CONFIG_ARGS:
                device_config_args[key] = value
            elif key in STC_DEVICE_STACK_ARGS:
                stack_args[key] = value
              
        device = self._stc.perform('DeviceCreateCommand', ParentList=self._project, **device_create_args)

        if len(device_config_args):
            self._stc.config(device['ReturnList'], **device_config_args)

        if stack is True and len(stack_args): 
            #TO do: Handle any stack interface
            if(device_create_args['IfStack'].find('Ipv4If') != -1):
                stackIf = self._stc.get(device['ReturnList'], 'children-Ipv4If')
                self._stc.config(stackIf, **stack_args)
        return device
