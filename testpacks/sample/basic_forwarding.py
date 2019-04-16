import time

from pkg.testbase.testbase import TestBase

#############################################################################
# Sample python TestCenter script to perform a two port test on a DUT. The  #
# test sends unidirection traffic and verifies the DUT forwards all packets.#
#############################################################################

class basic_forwarding(TestBase):
    def __init__(self, output_dir, testbed_file):
        super().__init__(__name__, output_dir, testbed_file)

    def setup(self):
        super().setup()

        logger = self.logger
        stc = self.stc

        logger.info("Connecting to device")
        dut = self.testbed.devices['dut1']
        dut.connect()

    def run(self):
        logger = self.logger
        stc = self.stc
        project = stc.project()

        port1 = stc.port("stc-port1")
        port1_h = port1.handle

        phy_1 = stc.create(port1.stc_config['phy'], under=port1_h)
        stc.config(port1_h, {"ActivePhy-targets": phy_1})

        port2 = stc.port("stc-port2")
        port2_h = port2.handle

        phy_2 = stc.create(port2.stc_config['phy'], under=port2_h)
        stc.config(port2_h, {"ActivePhy-targets": phy_2})

        # Create Device Blocks, underlying interfaces and relationships
        logger.info("Creating Host Device Blocks")
        emulatedDevice_1 = stc.create("EmulatedDevice", under=project)
        ipv4If_1 = stc.create("Ipv4If", under=emulatedDevice_1, Address=str(port1.ipv4.ip),
                              PrefixLength=port1.ipv4.network.prefixlen, Gateway=port1.gateway)
        ethIIIf_1 = stc.create("EthIIIf", under=emulatedDevice_1, SourceMac="00:00:00:00:00:01")
        stc.config(emulatedDevice_1, {"TopLevelIf-targets": [ipv4If_1]})
        stc.config(emulatedDevice_1, {"PrimaryIf-targets": [ipv4If_1]})
        stc.config(ipv4If_1, {"StackedOnEndpoint-targets": [ethIIIf_1]})
        stc.config(port1_h, {"AffiliationPort-sources": [emulatedDevice_1]})

        emulatedDevice_2 = stc.create("EmulatedDevice", under=project)
        ipv4If_2 = stc.create("Ipv4If", under=emulatedDevice_2, Address=str(port2.ipv4.ip),
                              PrefixLength=port2.ipv4.network.prefixlen, Gateway=port2.gateway)
        ethIIIf_2 = stc.create("EthIIIf", under=emulatedDevice_2, SourceMac="00:00:00:00:00:02")
        stc.config(emulatedDevice_2, {"TopLevelIf-targets": [ipv4If_2]})
        stc.config(emulatedDevice_2, {"PrimaryIf-targets": [ipv4If_2]})
        stc.config(ipv4If_2, {"StackedOnEndpoint-targets": [ethIIIf_2]})
        stc.config(port2_h, {"AffiliationPort-sources": [emulatedDevice_2]})

        # Create Stream Block and set bindings so traffic sources from emulatedDevice_1
        # and targets emulatedDevice_2
        logger.info("Creating StreamBlock on Port 1")
        streamBlock = stc.create('streamBlock', under=port1_h)
        stc.config(streamBlock, {"SrcBinding-targets": [ipv4If_1]})
        stc.config(streamBlock, {"DstBinding-targets": [ipv4If_2]})

        # Apply test config
        stc.apply()

        logger.info("Configuring device")
        dut = self.testbed.devices['dut1']
        for intf in dut.interfaces.values():
            if intf.alias == 'port1':
                intf.ipv4 = "30.0.1.1/24"
            else:
                intf.ipv4 = "30.0.2.1/24"
            intf.build_config()

        # Subscribe to generator and analyzer results
        logger.info('Subscribing to results')
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port1_h,
                             ConfigType='Generator', resulttype='GeneratorPortResults',
                             filenameprefix='Generator_port1_counter')
        port1GeneratorResult = status['ReturnedDataSet']
        status = stc.perform('ResultsSubscribeCommand', Parent=project, ResultParent=port2_h,
                             ConfigType='Analyzer', resulttype='AnalyzerPortResults',
                             filenameprefix='Analyzer_port2_counter')
        port2AnalyzerResult = status['ReturnedDataSet']

        # Perform Arp on bound device blocks to resolve DUT mac addresses
        logger.info("Arping devices to resolve mac address")
        arpCmdStatus = stc.perform('ArpNdStartCommand', WaitForArpToFinish="TRUE", HandleList=project)
        if arpCmdStatus['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError("Error - One or more emulated devices failed to successfully ARP the DUT")

        ################################################################################
        # Send test traffic and verify that the DUT forwarded all packets with no loss #
        ################################################################################

        ########################
        # Configure generators #
        ########################
        logger.info("Configuring port1 generator")
        generator1 = stc.get(port1_h, 'children-Generator').split(' ')[0]
        generatorConfig1 = (stc.get(generator1, 'children-GeneratorConfig')).split(' ')[0]
        stc.config(generatorConfig1,
                   SchedulingMode="PORT_BASED",
                   Duration="60",
                   DurationMode="SECONDS",
                   BurstSize="1",
                   LoadUnit="PERCENT_LINE_RATE",
                   LoadMode="FIXED",
                   FixedLoad="10")

        #################################
        # Apply generator configuration #
        #################################
        logger.info("Applying generator configuration")
        stc.apply()

        #################
        # Start traffic #
        #################
        logger.info("Starting Traffic and wait for generator to stop")
        stc.perform('GeneratorStartCommand', GeneratorList=generator1)
        stc.perform('GeneratorWaitForStopCommand', GeneratorList=generator1, WaitTimeout="90")
        logger.info('sleeping for 5 seconds after generator stopped for residual traffic to get forwarded')
        time.sleep(5)

        #####################################################
        # Collect Tx Signature Frame and Rx Sig Frame Count #
        #####################################################
        genResult = (stc.get(port1GeneratorResult, 'ResultHandleList')).split(' ')[0]
        TxSigCount = stc.get(genResult, 'GeneratorSigFrameCount')
        analyzerresult = stc.get(port2AnalyzerResult, 'ResultHandleList').split(' ')[0]
        RxSigCount = stc.get(analyzerresult, 'SigFrameCount')

        if int(TxSigCount) == int(RxSigCount):
            msg = ''.join(['No frame loss detected: TxFrameCount = ', str(TxSigCount), ', RxFrameCount = ', str(RxSigCount)])
            logger.info(msg)
            return msg
        else:
            loss = int(TxSigCount) - int(RxSigCount)
            msg = ''.join(['Frame loss detected: ', 'TxFrameCount = ', str(TxSigCount), ', RxFrameCount = ', str(RxSigCount),
                          ', Frame Loss = ' + str(loss)])
            raise RuntimeError(msg)

    def cleanup(self):
        dut = self.testbed.devices['dut1']
        try:
            # TODO the following code shuts down the ports - check Genie docs on how to avoid that
            #for intf in dut.interfaces.values():
                #intf.shutdown = False
                #intf.build_unconfig()

            dut.disconnect()
        except Exception as e:
            self.logger.warning("DUT unconfigure: %s" % (str(e)))

        if self.stc is not None:
            self.stc.download_all_files(self.outdir)

        super().cleanup()
