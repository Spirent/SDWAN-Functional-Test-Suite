import time
import os
from pkg.testbase.testbase import TestBase
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from utility import stc_config_sdwan

#############################################################################
#                 SD_WAN_Path_Selection_L2_to_L4_Steering                   #
# 			   	    Topo : 3Stc1Dut_Type01		                            #
#############################################################################

class Path_Selection_L2_to_L4_Steering(TestBase):
    def run(self):
        test_case_name = 'SD_WAN_Path_Selection_L2_to_L4_Steering'

        logger = self.logger
        stc = self.stc
        project1 = stc.project()
        logger.info("Start to get values from yaml file.")

        configGLobal = stc_config_sdwan(self.testbed.custom.stc_config)
        configClientPort = stc_config_sdwan(list(self.testbed.devices['stc-client-port'].interfaces.values())[0].stc_config)
        configMplsPort = stc_config_sdwan(list(self.testbed.devices['stc-mpls-port'].interfaces.values())[0].stc_config)
        configInternetPort = stc_config_sdwan(list(self.testbed.devices['stc-inet-port'].interfaces.values())[0].stc_config)

        logger.info("Start to config port name for all ports.")
        #########################################
        # Config port objects #
        #########################################
        portClient = stc.port("stc-client-port")
        portHandleClient= portClient.handle
        stc.config(portHandleClient, {'Name': configClientPort.namePort})
        generatorClient = stc.get(portHandleClient, 'children-Generator')
        stc.config(stc.get(generatorClient, 'children-GeneratorConfig'), {'SchedulingMode': configClientPort.schedulingMode, 'DurationMode': configClientPort.durationMode, 'Duration': configClientPort.duration})

        portMpls = stc.port("stc-mpls-port")
        portHandleMpls = portMpls.handle
        stc.config(portHandleMpls, {'Name': configMplsPort.namePort})

        portInternet = stc.port("stc-inet-port")
        portHandleInternet= portInternet.handle
        stc.config(portHandleInternet, {'Name': configInternetPort.namePort})
        logger.info("Start to create all emulated device for all ports.")
        #########################
        # Config device objects #
        #########################
        deviceClient_Head = stc.device_config(Port=portHandleClient, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configClientPort.nameDevice1,Ipv4If={'Address':configClientPort.ipDevice1,'Gateway':configClientPort.gatewayDevice1})
        deviceClient_Device1 = stc.device_config(Port=portHandleClient, IfStack=configGLobal.ifStackDevice, DeviceCount=configClientPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configClientPort.nameDevice2,Ipv4If={'Address':configClientPort.ipDevice2})
        deviceClient_Device2 = stc.device_config(Port=portHandleClient, IfStack=configGLobal.ifStackDevice, DeviceCount=configClientPort.countDevice3, IfCount=configGLobal.ifCountDevice, Name=configClientPort.nameDevice3,Ipv4If={'Address':configClientPort.ipDevice3})
        deviceMpls_Head = stc.device_config(Port=portHandleMpls, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configMplsPort.nameDevice1,Ipv4If={'Address':configMplsPort.ipDevice1,'Gateway':configMplsPort.gatewayDevice1})
        deviceMpls_Device1 = stc.device_config(Port=portHandleMpls, IfStack=configGLobal.ifStackDevice, DeviceCount=configMplsPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configMplsPort.nameDevice2,Ipv4If={'Address':configMplsPort.ipDevice2})
        deviceInternet_Head = stc.device_config(Port=portHandleInternet, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configInternetPort.nameDevice1,Ipv4If={'Address':configInternetPort.ipDevice1,'Gateway':configInternetPort.gatewayDevice1})
        deviceInternet_Device1 = stc.device_config(Port=portHandleInternet, IfStack=configGLobal.ifStackDevice, DeviceCount=configInternetPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configInternetPort.nameDevice2,Ipv4If={'Address':configInternetPort.ipDevice2})

        ########################
        # Config links objects #
        ########################
        logger.info("Start to create and config all L3 forwarding Links for all emulated devices.")
        stc.perform('LinkCreate', SrcDev=deviceClient_Device1['ReturnList'], DstDev=deviceClient_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceClient_Device2['ReturnList'], DstDev=deviceClient_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceMpls_Device1['ReturnList'], DstDev=deviceMpls_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceInternet_Device1['ReturnList'], DstDev=deviceInternet_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        #########################
        # Config stream objects #
        #########################
        logger.info("Start to create and config all stream blocks for all emulated devices.")
        ipv4IfClient_Device1 = stc.get(deviceClient_Device1['ReturnList'], 'children-Ipv4If')
        ipv4IfClient_Device2 = stc.get(deviceClient_Device2['ReturnList'], 'children-Ipv4If')
        ipv4IfMpls_Device1 = stc.get(deviceMpls_Device1['ReturnList'], 'children-Ipv4If')
        ipv4IfInternet_Device1 = stc.get(deviceInternet_Device1['ReturnList'], 'children-Ipv4If')

        streamTCP01 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfInternet_Device1], 'Name': configClientPort.nameStream1, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode1, 'FrameConfig': configClientPort.frameConfigStream1})
        streamTCP02 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name': configClientPort.nameStream2, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode2, 'FrameConfig': configClientPort.frameConfigStream2})
        streamUDP01 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name': configClientPort.nameStream3, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode3, 'FrameConfig': configClientPort.frameConfigStream3})
        streamUDP02 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfInternet_Device1], 'Name': configClientPort.nameStream4, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode4, 'FrameConfig': configClientPort.frameConfigStream4})
        streamUDP03 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfInternet_Device1], 'Name': configClientPort.nameStream5, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FixedFrameLength': configClientPort.fixedFrameLength5, 'FrameConfig': configClientPort.frameConfigStream5})
        streamUDP04 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name': configClientPort.nameStream6, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FixedFrameLength': configClientPort.fixedFrameLength6, 'FrameConfig': configClientPort.frameConfigStream6})
        streamUDP05 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfInternet_Device1], 'Name': configClientPort.nameStream7, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode7, 'FrameConfig': configClientPort.frameConfigStream7})
        streamUDP06 = stc.create('streamBlock', under=portHandleClient, attributes={'SrcBinding-targets': [ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name': configClientPort.nameStream8, 'LoadUnit': configGLobal.loadUnitStream, "Load": configGLobal.loadStream, 'FrameLengthMode': configClientPort.frameLengthMode8, 'FrameConfig': configClientPort.frameConfigStream8})
        logger.info("Start to config modifiers for all stream blocks.")
        ranger_modifer_UDP03 = stc.create('RangeModifier', under=streamUDP03)
        ranger_modifer_UDP04 = stc.create('RangeModifier', under=streamUDP04)
        ranger_modifer_UDP05 = stc.create('RangeModifier', under=streamUDP05)
        ranger_modifer_UDP06 = stc.create('RangeModifier', under=streamUDP06)
        stc.config(ranger_modifer_UDP03, configClientPort.rangeModifierStream5)
        stc.config(ranger_modifer_UDP04, configClientPort.rangeModifierStream6)
        stc.config(ranger_modifer_UDP05, configClientPort.rangeModifierStream7)
        stc.config(ranger_modifer_UDP06, configClientPort.rangeModifierStream8)

        # get exact imix distribution
        system_imix_type_list = stc.get(project1, 'children-FrameLengthDistribution').split(' ')
        for imix_distribution in system_imix_type_list:
            name = stc.get(imix_distribution, 'name')
            if (configClientPort.frameLengthDistribution1 == name):
                stc.config(streamTCP01, {"AffiliationFrameLengthDistribution": imix_distribution})
            if (configClientPort.frameLengthDistribution2 == name):
                stc.config(streamTCP02, {"AffiliationFrameLengthDistribution": imix_distribution})
            if (configClientPort.frameLengthDistribution3 == name):
                stc.config(streamUDP01, {"AffiliationFrameLengthDistribution": imix_distribution})
            if (configClientPort.frameLengthDistribution4 == name):
                stc.config(streamUDP02, {"AffiliationFrameLengthDistribution": imix_distribution})
            if (configClientPort.frameLengthDistribution7 == name):
                stc.config(streamUDP05, {"AffiliationFrameLengthDistribution": imix_distribution})
            if (configClientPort.frameLengthDistribution8 == name):
                stc.config(streamUDP06, {"AffiliationFrameLengthDistribution": imix_distribution})
        logger.info("Apply all configuration to IL.")

        stc.perform('SaveAsXml', filename=test_case_name + '.xml')

        stc.apply()
        # calculate the first sum value for mpls port
        mpls_stream_frames = 0
        inet_stream_frames = 0
        tx_result_data_dict = {}
        rx_result_data_dict = {}

        ###################################
        # Start Arp and verify Arp status #
        ###################################
        logger.info("Start Arp.")
        arpStatus = stc.perform('ArpNdStartCommand', WaitForArpToFinish="TRUE", HandleList=project1)
        logger.info('======arp status is {0}======'.format(arpStatus['ArpNdState']))
        if arpStatus['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError('Arp failed, please check all configuration for both STC and DUT.')
        ###################################
        # Clear results and start traffic #
        ###################################
        logger.info("Clear all results for all ports.")
        stc.perform('ResultsClearAllCommand', PortList=project1)
        time.sleep(2)
        generator_1 = stc.get(portHandleClient, "children-Generator")
        logger.info("Start traffic.")
        stc.perform('GeneratorStartCommand', GeneratorList=[generator_1])
        stc.perform('GeneratorWaitForStartCommand', GeneratorList=generator_1, WaitTimeout="10")
        # wait enough time for traffic stop
        time.sleep(62)
        time.sleep(5)
        stc.perform("SaveResultsCommand", {'SaveDetailedResults': True, 'ResultFileName': 'detailed_result.db'})
        logger.info("Calculate Tx frame for stream block 1,4,5,7  = Rx frame for internet-port.")
        logger.info("Calculate Tx frame for stream block 2,3,6,8  = Rx frame for mpls-port.")
        # add counter for every streamblock
        for single_block in stc.get(portHandleClient, "children-streamblock").split(' '):
            stream_name = stc.get(single_block, "name")
            # create a counter for tx frame count
            tx_result_data_set = stc.perform('ResultsSubscribeCommand', Parent=project1, ResultParent=single_block,\
                    ConfigType='StreamBlock', ResultType='txstreamblockresults', interval='1')['ReturnedDataSet']
            tx_result_data_dict[stream_name] = tx_result_data_set
            # create a counter for rx frame loss
            rx_result_data_set = stc.perform('ResultsSubscribeCommand', Parent=project1, ResultParent=single_block,\
                    ConfigType='StreamBlock', ResultType='rxstreamblockresults', interval='1')['ReturnedDataSet']
            rx_result_data_dict[stream_name] = rx_result_data_set

        resultPortMpls = stc.perform('ResultsSubscribeCommand', Parent=project1, ResultParent=portHandleMpls, \
                                     ConfigType='Analyzer', ResultType='AnalyzerPortResults')['ReturnedDataSet']
        resultPortInternet = stc.perform('ResultsSubscribeCommand', Parent=project1, ResultParent=portHandleInternet, \
                                         ConfigType='Analyzer', ResultType='AnalyzerPortResults')['ReturnedDataSet']
        # for result_handle in handle_list:
        # the stream 2,3,6,8
        mpls_list = ["TCP02", "UDP01", "UDP04", "UDP06"]
        for stream_name, result_object in tx_result_data_dict.items():
            result_handle = stc.get(result_object, "ResultHandleList").split(' ')[0]
            if stream_name in mpls_list:
                mpls_frame_count = stc.get(result_handle, 'Framecount')
                mpls_stream_frames += int(mpls_frame_count)
            else:
                inet_frame_count = stc.get(result_handle, 'Framecount')
                inet_stream_frames += int(inet_frame_count)
        frame_loss_list = []
        frames_loss_count = 0
        for stream_name, result_object in rx_result_data_dict.items():
            result_handle = stc.get(result_object, "ResultHandleList").split(' ')[0]
            if stream_name in mpls_list:
                mpls_frame_loss = stc.get(result_handle, 'DroppedFrameCount')
                frame_loss_list.append(mpls_frame_loss)
                frames_loss_count += int(mpls_frame_loss)
            else:
                inet_frame_loss = stc.get(result_handle, 'DroppedFrameCount')
                frame_loss_list.append(inet_frame_loss)
                frames_loss_count += int(inet_frame_loss)

        rx_mpls_count = int(stc.get(stc.get(resultPortMpls, 'ResultHandleList').split(' ')[0], 'SigFrameCount'))
        rx_inet_count = int(stc.get(stc.get(resultPortInternet, 'ResultHandleList').split(' ')[0], 'SigFrameCount'))

        if rx_mpls_count == mpls_stream_frames:
            logger.info("Mpls port received all related frames from client port correctly.")
        else:
            raise RuntimeError("Mpls port can't receive all frames which send by client port. \
            RxFrameCount: %d, TxFrameCount: %d" % (rx_mpls_count,mpls_stream_frames))

        if rx_inet_count == inet_stream_frames:
            logger.info("Inet port received all related frames from client port correctly.")
        else:
            raise RuntimeError("Inet port can't receive all frames which send by client port.")
        logger.info("Check whether there is frame loss or not.")
        if frames_loss_count > 0:
            raise RuntimeError("There are frame loss for all stream blocks. Frame loss for every stream block is as \
                    blow: %s" % str(frame_loss_list))

        testMsg = "No frame loss for all stream blocks"

        # save all results database for this testing
        stc.perform("SaveResultCommand", {'SaveDetailedResults': True})
        return testMsg
