import os, sys, subprocess
import time
from pkg.testbase.testbase import TestBase
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from utility import stc_config_sdwan

class Resiliency_Link_Blackout_Remote_no_Congestion(TestBase):
    def run(self):
        logger = self.logger
        stc = self.stc
        sne = self.sne.devices['sne']
        project = stc.project()
        ######################################
        # Define parameters related to cases #
        ######################################
        configGLobal = stc_config_sdwan(self.testbed.custom.stc_config)
        configClientPort = stc_config_sdwan(list(self.testbed.devices['stc-client-port'].interfaces.values())[0].stc_config)
        configMplsPort = stc_config_sdwan(list(self.testbed.devices['stc-mpls-port'].interfaces.values())[0].stc_config)
        configInternetPort = stc_config_sdwan(list(self.testbed.devices['stc-inet-port'].interfaces.values())[0].stc_config)
        sneConfigFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.test_input.sne_config_file)
        waitTimesAfterBreakLink = int(configGLobal.waitTimeAfterBreakLink / configGLobal.waitIntervalAfterBreakLink)
        waitTimesAfterRecoverLink = int(configGLobal.waitTimeAfterRecoverLink / configGLobal.waitIntervalAfterRecoverLink)
        #########################################
        # Config port objects and reserve ports #
        #########################################
        portClient = stc.port("stc-client-port")
        portHandleClient= portClient.handle
        stc.config(portHandleClient, {'Name':configClientPort.namePort})
        generatorClient = stc.get(portHandleClient, 'children-Generator')
        stc.config(stc.get(generatorClient, 'children-GeneratorConfig'), {'LoadUnit': configClientPort.loadUnitPort, 'FixedLoad': configClientPort.fixedLoadPort})

        portMpls = stc.port("stc-mpls-port")
        portHandleMpls = portMpls.handle
        stc.config(portHandleMpls, {'Name':configMplsPort.namePort})

        portInternet = stc.port("stc-inet-port")
        portHandleInternet= portInternet.handle
        stc.config(portHandleInternet, {'Name':configInternetPort.namePort})
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
        stc.perform('LinkCreate', SrcDev=deviceClient_Device1['ReturnList'], DstDev=deviceClient_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceClient_Device2['ReturnList'], DstDev=deviceClient_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceMpls_Device1['ReturnList'], DstDev=deviceMpls_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=deviceInternet_Device1['ReturnList'], DstDev=deviceInternet_Head['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        #########################
        # Config stream objects #
        #########################
        ipv4IfClient_Device1 = stc.get(deviceClient_Device1['ReturnList'], 'children-Ipv4If')
        ipv4IfClient_Device2 = stc.get(deviceClient_Device2['ReturnList'], 'children-Ipv4If')
        ipv4IfMpls_Device1 = stc.get(deviceMpls_Device1['ReturnList'], 'children-Ipv4If')
        streamTCP01 = stc.create('streamBlock',under=portHandleClient,attributes={'SrcBinding-targets':[ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name':configClientPort.nameStream1, 'FixedFrameLength':configGLobal.frameLength, 'FrameConfig':configClientPort.frameConfigStream1})
        streamTCP02 = stc.create('streamBlock',under=portHandleClient,attributes={'SrcBinding-targets':[ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name':configClientPort.nameStream2, 'FixedFrameLength':configGLobal.frameLength, 'FrameConfig':configClientPort.frameConfigStream2})
        streamUDP01 = stc.create('streamBlock',under=portHandleClient,attributes={'SrcBinding-targets':[ipv4IfClient_Device1], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name':configClientPort.nameStream3, 'FixedFrameLength':configGLobal.frameLength, 'FrameConfig':configClientPort.frameConfigStream3})
        streamUDP02 = stc.create('streamBlock',under=portHandleClient,attributes={'SrcBinding-targets':[ipv4IfClient_Device2], 'DstBinding-targets':[ipv4IfMpls_Device1], 'Name':configClientPort.nameStream4, 'FixedFrameLength':configGLobal.frameLength, 'FrameConfig':configClientPort.frameConfigStream4})
        ranger_modifer_UDP01 = stc.create('RangeModifier', under=streamUDP01)
        ranger_modifer_UDP02 = stc.create('RangeModifier', under=streamUDP02)
        stc.config(ranger_modifer_UDP01, configClientPort.rangeModifierStream3)
        stc.config(ranger_modifer_UDP02, configClientPort.rangeModifierStream4)
        #########################
        # Apply and save config #
        #########################
        stc.apply()
        stc.perform('saveasxml',filename='StcConfig.xml')
        #####################
        # Subscribe results #
        #####################
        resultPortClient = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=portHandleClient, ConfigType='Generator', ResultType='GeneratorPortResults')['ReturnedDataSet']
        resultPortMpls = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=portHandleMpls, ConfigType='Analyzer', ResultType='AnalyzerPortResults')['ReturnedDataSet']
        resultPortInternet = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=portHandleInternet, ConfigType='Analyzer', ResultType='AnalyzerPortResults')['ReturnedDataSet']
        ###################################
        # Start Arp and verify Arp status #
        ###################################
        arpStatus = stc.perform('ArpNdStartCommand', WaitForArpToFinish="TRUE", HandleList=project)
        if arpStatus['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError('Arp failed, please check all configuration for both STC and DUT.')
        ##########################################################
        # Start traffic and verify traffic goes via correct link #
        ##########################################################
        logger.info('Start Traffic and verify traffic goes via correct link')
        #<=========Start stream which should go via Internet link and verify result===========>
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        stc.perform('StreamBlockStartCommand', StreamBlockList=[streamTCP01,streamUDP01])
        time.sleep(3)
        stc.perform('StreamBlockStopCommand', StreamBlockList=[streamTCP01,streamUDP01])
        time.sleep(2)
        txSigCountClient = stc.get(stc.get(resultPortClient, 'ResultHandleList').split(' ')[0], 'GeneratorSigFrameCount')
        rxSigCountInternet = stc.get(stc.get(resultPortInternet, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        if txSigCountClient != rxSigCountInternet:
            raise RuntimeError('Stream named TCP02 and UDP02 should be forwarded via Internet Link, actually send {0} packets from Client port and get {1} packets from Internet port.'.format(txSigCountClient, rxSigCountInternet))
        else:
            logger.info('======Traffic go via Internet link correctly======')
        #<=========Start stream which should go via Mpls link and verify result===========>
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        stc.perform('StreamBlockStartCommand', StreamBlockList=[streamTCP02,streamUDP02])
        time.sleep(3)
        stc.perform('StreamBlockStopCommand', StreamBlockList=[streamTCP02,streamUDP02])
        time.sleep(2)
        txSigCountClient = stc.get(stc.get(resultPortClient, 'ResultHandleList').split(' ')[0], 'GeneratorSigFrameCount')
        rxSigCountMpls = stc.get(stc.get(resultPortMpls, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        if txSigCountClient != rxSigCountMpls:
            raise RuntimeError('Stream named TCP01 and UDP01 should be forwarded via Mpls Link, actually send {0} packets from Client port and get {1} packets from Mpls port.'.format(txSigCountClient, rxSigCountMpls))
        else:
            logger.info('======Traffic go via Mpls link correctly======')
        ##########################################################################
        # Blackout Internet link by SNE, then traffic should switch to Mpls link #
        ##########################################################################
        txTrafficRate = int(stc.get(stc.get(generatorClient, 'children-GeneratorConfig'), 'FpsLoad'))
        totalTrafficRate = int(txTrafficRate * 0.9)
        #<=========Start traffic===========>
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        stc.perform('GeneratorStartCommand', GeneratorList=generatorClient)
        #<=========Blackout Internet link by SNE and verify result===========>
        logger.info('Start Sne to blackout Internet link')
        sne.configure()
        sne.upload(config_file=sneConfigFile)
        sne.start()
        for i in range(waitTimesAfterBreakLink):
            time.sleep(configGLobal.waitIntervalAfterBreakLink)
            rxSigRateMpls = stc.get(stc.get(resultPortMpls, 'ResultHandleList').split(' ')[0], 'SigFrameRate')
            if int(rxSigRateMpls) > totalTrafficRate:
                break
            if i==(waitTimesAfterBreakLink - 1):
                raise RuntimeError('Traffic can not switch to Mpls link in {0}s after blackout Internet link'.format(configGLobal.waitTimeAfterBreakLink))
        stc.perform('GeneratorStopCommand', GeneratorList=generatorClient)
        time.sleep(2)
        txSigCountClient = stc.get(stc.get(resultPortClient, 'ResultHandleList').split(' ')[0], 'GeneratorSigFrameCount')
        rxSigCountMpls = stc.get(stc.get(resultPortMpls, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        rxSigCountInternet = stc.get(stc.get(resultPortInternet, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        timeSwitch = int((int(txSigCountClient) - int(rxSigCountMpls) - int(rxSigCountInternet)) * 1000 / txTrafficRate)
        logger.info('======Traffic switch to mpls link successfully after blackout internet link and Out of service time is {0} ms======\n'.format(timeSwitch))
        msgRobot = '======Traffic switch to mpls link successfully after blackout internet link and Out of service time is {0} ms======\n'.format(timeSwitch)
        ##################################################################################
        # Recover Internet link by SNE, then traffic should switch back to Internet link #
        ##################################################################################
        halfTrafficRate = int(totalTrafficRate / 2)
        #<=========Start traffic===========>
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        #<=========Recover Internet link by SNE and verify result===========>
        stc.perform('GeneratorStartCommand', GeneratorList=generatorClient)
        sne.stop()
        for i in range(waitTimesAfterRecoverLink):
            time.sleep(configGLobal.waitIntervalAfterRecoverLink)
            rxSigRateInternet = stc.get(stc.get(resultPortInternet, 'ResultHandleList').split(' ')[0], 'SigFrameRate')
            if int(rxSigRateInternet) > halfTrafficRate:
                break
            if i==(waitTimesAfterRecoverLink - 1):
                raise RuntimeError('Traffic can not switch back to Internet link in {0}s after recover Internet link'.format(configGLobal.waitTimeAfterRecoverLink))
        stc.perform('GeneratorStopCommand', GeneratorList=generatorClient)
        time.sleep(2)
        txSigCountClient = stc.get(stc.get(resultPortClient, 'ResultHandleList').split(' ')[0], 'GeneratorSigFrameCount')
        rxSigCountMpls = stc.get(stc.get(resultPortMpls, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        rxSigCountInternet = stc.get(stc.get(resultPortInternet, 'ResultHandleList').split(' ')[0], 'SigFrameCount')
        timeSwitch = int((int(txSigCountClient) - int(rxSigCountMpls) - int(rxSigCountInternet)) * 1000 / txTrafficRate)
        logger.info('======Traffic switch back to Internet link successfully after recover internet link and recovery time is {0} ms======\n'.format(timeSwitch))
        msgRobot = msgRobot + '======Traffic switch back to Internet link successfully after recover internet link and recovery time is {0} ms======\n'.format(timeSwitch)
        return msgRobot
