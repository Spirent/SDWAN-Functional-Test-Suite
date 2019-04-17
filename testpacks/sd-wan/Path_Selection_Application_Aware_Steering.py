import os, sys, subprocess
import time
from pkg.testbase.testbase import TestBase
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from utility import stc_config_sdwan

class path_selection_application_aware_steering(TestBase):
    def __init__(self, output_dir, testbed_file):
        super().__init__(__name__, output_dir, testbed_file)

    def setup(self):
        super().setup()
        logger = self.logger
        stc = self.stc
        trs = stc.get(stc.project(), 'children-TestResultSetting')

    def run(self):
        logger = self.logger
        stc = self.stc
        project = stc.project()
        msgRobot = ''
        
        #######################
        # Configuration phase #
        #######################
        configGLobal = stc_config_sdwan(self.testbed.custom.stc_config)
        configClientPort = stc_config_sdwan(list(self.testbed.devices['stc-client-port'].interfaces.values())[0].stc_config)
        configMplsPort = stc_config_sdwan(list(self.testbed.devices['stc-mpls-port'].interfaces.values())[0].stc_config)
        configInternetPort = stc_config_sdwan(list(self.testbed.devices['stc-inet-port'].interfaces.values())[0].stc_config)
        ### Configure ports ###
        logger.info("Configuring STC ports")
        port1 = stc.port("stc-client-port")
        clientporthandle = port1.handle
        stc.config (clientporthandle, {'Name': 'Client'})
        
        if port1.stc_config['Phy'] is True:
            phy_1 = stc.create(port1.stc_config['Phy'], under=clientporthandle)
            stc.config(clientporthandle, {"ActivePhy-targets": phy_1})

        port2 = stc.port("stc-mpls-port")
        mplsporthandle = port2.handle
        stc.config (mplsporthandle, {'Name': 'MPLS'})

        if port2.stc_config['Phy'] is True:
            phy_2 = stc.create(port2.stc_config['Phy'], under=mplsporthandle)
            stc.config(mplsporthandle, {"ActivePhy-targets": phy_2})

        port3 = stc.port("stc-inet-port")
        inetporthandle = port3.handle
        stc.config (inetporthandle, {'Name': 'Internet'})

        if port3.stc_config['Phy'] is True:
            phy_3 = stc.create(port3.stc_config['Phy'], under=inetporthandle)
            stc.config(inetporthandle, {"ActivePhy-targets": phy_3})
        
        ### Creating devices ###
        logger.info("Creating devices") 
        client_dummydevice = stc.device_config(Port=clientporthandle, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name='Client-dummy')
        client_headdevice = stc.device_config(Port=clientporthandle, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configClientPort.nameDevice1,Address=configClientPort.ipDevice1,Gateway=configClientPort.gatewayDevice1)
        client_device1device = stc.device_config(Port=clientporthandle, IfStack=configGLobal.ifStackDevice, DeviceCount=configClientPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configClientPort.nameDevice2,Address=configClientPort.ipDevice2, Gateway=configClientPort.gatewayDevice2)
        mpls_headdevice = stc.device_config(Port=mplsporthandle, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configMplsPort.nameDevice1,Address=configMplsPort.ipDevice1,Gateway=configMplsPort.gatewayDevice1)
        mpls_device1device = stc.device_config(Port=mplsporthandle, IfStack=configGLobal.ifStackDevice, DeviceCount=configMplsPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configMplsPort.nameDevice2,Address=configMplsPort.ipDevice2, Gateway=configMplsPort.gatewayDevice2)
        inet_headdevice = stc.device_config(Port=inetporthandle, IfStack=configGLobal.ifStackDevice, IfCount=configGLobal.ifCountDevice, Name=configInternetPort.nameDevice1,Address=configInternetPort.ipDevice1,Gateway=configInternetPort.gatewayDevice1)
        inet_device1device = stc.device_config(Port=inetporthandle, IfStack=configGLobal.ifStackDevice, DeviceCount=configInternetPort.countDevice2, IfCount=configGLobal.ifCountDevice, Name=configInternetPort.nameDevice2,Address=configInternetPort.ipDevice2, Gateway=configInternetPort.gatewayDevice2)
        
        ### Create links ###
        logger.info("Creating links")
        stc.perform('LinkCreate', SrcDev=client_device1device['ReturnList'], DstDev=client_headdevice['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=client_dummydevice['ReturnList'], DstDev=client_headdevice['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=mpls_device1device['ReturnList'], DstDev=mpls_headdevice['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        stc.perform('LinkCreate', SrcDev=inet_device1device['ReturnList'], DstDev=inet_headdevice['ReturnList'], LinkType=configGLobal.linkTypeDevice)
        
        ### Configure device-level HTTP ###
        logger.info("Configuring HTTP protocol")
        httpclientload_loadtype = configGLobal.httpClientLoadType
        httpclientload_maxconnectionsattempted = configGLobal.httpClientMaxConnectionsAttempted
        httpclientload_maxtransactionsattempted = 10 * httpclientload_maxconnectionsattempted
        httpclientload_maxopenconnections = configGLobal.httpClientMaxOpenConnections
        httpserver_inet = stc.create('HttpServerProtocolConfig', under = inet_device1device['ReturnList'], Name='HTTP Server Internet', ServerName='HTTP Server Internet')
        httpserver_mpls = stc.create('HttpServerProtocolConfig', under = mpls_device1device['ReturnList'], Name='HTTP Server MPLS', ServerName='HTTP Server MPLS')
        httpclient = stc.create("HttpClientProtocolConfig", under = client_device1device['ReturnList'], Name='HTTP Client')
        httpclient_dummy = stc.create("HttpClientProtocolConfig", under = client_dummydevice['ReturnList'], Name='HTTP Dummy Client')
        stc.config(httpclient,{"ConnectionDestination-targets" :httpserver_inet})
        stc.config(httpclient_dummy,{"ConnectionDestination-targets" :httpserver_mpls})
        
        ### Configure HTTP profiles ###
        logger.info("Configuring HTTP profiles")
        httpclientload = stc.create('ClientLoadProfile', under=project, MaxConnectionsAttempted=httpclientload_maxconnectionsattempted, \
        LoadType=httpclientload_loadtype, MaxOpenConnections=httpclientload_maxopenconnections, ProfileName="HTTP client load profile")
        ## phase1 ##
        httploadphase_1 = stc.create("ClientLoadPhase",under = httpclientload, PhaseName="Delay", PhaseNum="1", LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor",under = httploadphase_1, Height="0", RampTime="0", SteadyTime="5", Active="TRUE", LocalActive="TRUE")
        ## phase2 ##
        httploadphase_2 = stc.create("ClientLoadPhase",under = httpclientload, PhaseName="Ramp Up", PhaseNum="2", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor",under = httploadphase_2, Height="10", Repetitions="1", RampTime="10", SteadyTime="0", Active="TRUE", LocalActive="TRUE")
        ## phase3 ##
        httploadphase_3 = stc.create("ClientLoadPhase",under = httpclientload, PhaseName="Stair Step", PhaseNum="3", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor",under = httploadphase_3, Height="4", Repetitions="5", RampTime="5", SteadyTime="5", Active="TRUE", LocalActive="TRUE")
        ## phase4 ##
        httploadphase_4 = stc.create("ClientLoadPhase",under = httpclientload, PhaseName="Steady State", PhaseNum="4", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor",under = httploadphase_4, Height="0", Repetitions="1", RampTime="0", SteadyTime="30", Active="TRUE", LocalActive="TRUE")
        ## phase5 ##
        httploadphase_5 = stc.create("ClientLoadPhase",under = httpclientload, PhaseName="Ramp Down", PhaseNum="5", LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor",under = httploadphase_5, Height="0", RampTime="0", SteadyTime="20", Active="TRUE", LocalActive="TRUE")
        stc.config(httpclient,{"AffiliatedClientLoadProfile-targets" : [httpclientload]})
        
        ### Configure device-level SIP ###
        logger.info("Configuring SIP protocol")
        sipcaller_uanumberformat = configClientPort.sipUaNumFormatDevice2
        sipcallee_uanumberformat = configMplsPort.sipUaNumFormatDevice2
        sipload_loadtype = configGLobal.sipClientLoadType
        sipload_maxopenconnections = configGLobal.sipClientMaxOpenConnections
        sipload_maxconnectionsattempted = configGLobal.sipClientMaxConnectionsAttempted
        sipcallee = stc.create('SipUaProtocolconfig', under=mpls_device1device['ReturnList'], UaNumFormat=sipcallee_uanumberformat, Name='SIP Callee')
        sipcaller = stc.create('SipUaProtocolconfig', under=client_device1device['ReturnList'], UaNumFormat=sipcaller_uanumberformat, Name='SIP Caller')
        
        ### Configure SIP call profile and load profile ###
        logger.info("Configuring SIP profiles")
        client_device1ipv4if = stc.get(client_device1device['ReturnList'], 'children-Ipv4If')
        siploadprofile = stc.create('ClientLoadProfile', under=project, ProfileName="SIP_LoadProfile_1", LoadType=sipload_loadtype, MaxConnectionsAttempted=sipload_maxconnectionsattempted, MaxOpenConnections=sipload_maxopenconnections)
        siploadphase_1 = stc.create("ClientLoadPhase",under = siploadprofile, PhaseName="Label 1", PhaseNum="1", LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor",under = siploadphase_1, Height="4", RampTime="180", SteadyTime="0", Active="TRUE", LocalActive="TRUE")
        sipcallerprofile = stc.create ('ClientProfile', under = project, ProfileName="SIP_ClientProfile_1" )
        stc.create("SipUaProtocolProfile",under = sipcallerprofile, CallTime="3")
        stc.config(sipcaller,{"ConnectionDestination-targets" : [sipcallee], "UsesIf-targets" :[client_device1ipv4if]})
        stc.config(sipcaller,{"AffiliatedClientLoadProfile-targets" : [siploadprofile]})
        stc.config(sipcaller,{"AffiliatedClientProfile-targets" : [sipcallerprofile]})
        stc.config(sipcallee,{"AffiliatedClientProfile-targets" : [sipcallerprofile]})
        
        ### Configure sequencer commands ###
        logger.info("Configuring command sequencer")
        sequencer = stc.create("Sequencer",under='system1', ErrorHandler='STOP_ON_ERROR')
        clearallresultatbeginning = stc.create("ResultsClearAllCommand",under=sequencer, Name='Clear all results before start testing')
        arpatbeginning = stc.create('ArpNdStartOnAllDevicesCommand', under=sequencer, Name='Start ARP on all devices')
        verifyarpstatus = stc.create ('ArpNdVerifyResolvedCommand', under=sequencer, HandleList=[client_headdevice['ReturnList'], mpls_headdevice['ReturnList'], inet_headdevice['ReturnList']])
        starthttpserver = stc.create('ProtocolStartCommand', under=sequencer, Name='Start HTTP server', ProtocolList=[httpserver_inet, httpserver_mpls])
        waithttpserver = stc.create ('WaitCommand', under=sequencer, Name='Wait for HTTP server to be brought up', WaitTime='10')
        starthttpclient = stc.create('ProtocolStartCommand', under=sequencer, Name='Start HTTP client', ProtocolList=[httpclient])
        waithttpclient = stc.create ('WaitCommand', under=sequencer, Name='Wait for HTTP client to be brought up', WaitTime='20')       
        ## Verify HTTP results ##
        verifyhttpresult = stc.create ('VerifyResultsValueCommand', under=sequencer, WaitTimeout="180", ErrorOnFailure='TRUE', Name='Verify HTTP results')
        # Condition 1 #
        httpresultdataset_1 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        httpresultquery_1 = stc.create ('ResultQuery', under=httpresultdataset_1, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.attemptedconnections")
        stc.config (httpresultquery_1, ResultRootList=httpclient, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="AttemptedConnections", ValueOperand=httpclientload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxconnectionsattempted, MaxValueOperand=httpclientload_maxconnectionsattempted, ResultQuery=httpresultquery_1)
        # Condition 2 #
        httpresultdataset_2 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        httpresultquery_2 = stc.create ('ResultQuery', under=httpresultdataset_2, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.attemptedtransactions")
        stc.config (httpresultquery_2, ResultRootList=httpclient, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="AttemptedTransactions", ValueOperand=httpclientload_maxtransactionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxtransactionsattempted, MaxValueOperand=httpclientload_maxtransactionsattempted, ResultQuery=httpresultquery_2)
        # Condition 3 #
        httpresultdataset_3 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        httpresultquery_3 = stc.create ('ResultQuery', under=httpresultdataset_3, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.successfultransactions")
        stc.config (httpresultquery_3, ResultRootList=httpclient, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="SuccessfulTransactions", ValueOperand=httpclientload_maxtransactionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxtransactionsattempted, MaxValueOperand=httpclientload_maxtransactionsattempted, ResultQuery=httpresultquery_3)
        # Condition 4 #
        httpresultdataset_4 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        httpresultquery_4 = stc.create ('ResultQuery', under=httpresultdataset_4, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.successfulconnections")
        stc.config (httpresultquery_4, ResultRootList=httpclient, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="Successfulconnections", ValueOperand=httpclientload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxconnectionsattempted, MaxValueOperand=httpclientload_maxconnectionsattempted, ResultQuery=httpresultquery_4)
        # Condition 5 #
        httpresultdataset_5 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpServerProtocolConfig")
        httpresultquery_5 = stc.create ('ResultQuery', under=httpresultdataset_5, ConfigClassId="httpserverprotocolconfig", ResultClassId="httpserverresults", PropertyIdArray="httpserverresults.successfultransactions")
        stc.config (httpresultquery_5, ResultRootList=httpserver_inet, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="SuccessfulTransactions", ValueOperand=httpclientload_maxtransactionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxtransactionsattempted, MaxValueOperand=httpclientload_maxtransactionsattempted, ResultQuery=httpresultquery_5)
        # Condition 6 #
        httpresultdataset_6 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpServerProtocolConfig")
        httpresultquery_6 = stc.create ('ResultQuery', under=httpresultdataset_6, ConfigClassId="httpserverprotocolconfig", ResultClassId="httpserverresults", PropertyIdArray="httpserverresults.Totalconnections")
        stc.config (httpresultquery_6, ResultRootList=httpserver_inet, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifyhttpresult, PropertyOperand="Totalconnections", ValueOperand=httpclientload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=httpclientload_maxconnectionsattempted, MaxValueOperand=httpclientload_maxconnectionsattempted, ResultQuery=httpresultquery_6)
        ## Stop HTTP client and server ##
        stophttpserver = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop HTTP server', ProtocolList=[httpserver_inet, httpserver_mpls])
        stophttpclient = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop HTTP client', ProtocolList=[httpclient])
        ## Start SIP caller ##
        startsipcaller = stc.create('ProtocolStartCommand', under=sequencer, Name='Start SIP caller', ProtocolList=[sipcaller])
        waitsipcaller = stc.create ('WaitCommand', under=sequencer, Name='Wait for SIP caller to be brought up', WaitTime='10')
        ## Verify SIP results ##
        verifysipresult = stc.create ('VerifyResultsValueCommand', under=sequencer, WaitTimeout="300", ErrorOnFailure='TRUE', Name='Verify SIP results')
        # Condition 1 #
        sipresultdataset_1 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sipresultquery_1 = stc.create ('ResultQuery', under=sipresultdataset_1, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callattemptcount")
        stc.config (sipresultquery_1, ResultRootList=sipcaller, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifysipresult, PropertyOperand="CallAttemptCount", ValueOperand=sipload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sipload_maxconnectionsattempted, MaxValueOperand=sipload_maxconnectionsattempted, ResultQuery=sipresultquery_1)
        # Condition 2 #
        sipresultdataset_2 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sipresultquery_2 = stc.create ('ResultQuery', under=sipresultdataset_2, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callsuccesscount")
        stc.config (sipresultquery_2, ResultRootList=sipcaller, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifysipresult, PropertyOperand="CallSuccessCount", ValueOperand=sipload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sipload_maxconnectionsattempted, MaxValueOperand=sipload_maxconnectionsattempted, ResultQuery=sipresultquery_2)
        # Condition 3 #
        sipresultdataset_3 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sipresultquery_3 = stc.create ('ResultQuery', under=sipresultdataset_3, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callsansweredcount")
        stc.config (sipresultquery_3, ResultRootList=sipcallee, PropertyHandleArray="")
        stc.create ('VerifyResultsValueCondition', under=verifysipresult, PropertyOperand="CallsAnsweredCount", ValueOperand=sipload_maxconnectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sipload_maxconnectionsattempted, MaxValueOperand=sipload_maxconnectionsattempted, ResultQuery=sipresultquery_3)
        ## Stop SIP caller ##
        stopsipcaller = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop SIP caller', ProtocolList=[sipcaller])
        stc.config(sequencer,CommandList=[clearallresultatbeginning, arpatbeginning, verifyarpstatus, starthttpserver, waithttpserver, starthttpclient, waithttpclient, verifyhttpresult, stophttpserver, stophttpclient, startsipcaller, waitsipcaller, verifysipresult, stopsipcaller])
        
        ######################
        # Subcscribe results #
        ######################
        logger.info("Subscribing results")        
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='httpclientprotocolconfig', resultType='httpclientresults', filenamePrefix='sdwan-path-selection-0002-httpclientresults')
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='httpserverprotocolconfig', resultType='httpserverresults', filenamePrefix='sdwan-path-selection-0002-httpserverresults')
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='sipuaprotocolconfig', resultType='sipuaresults', filenamePrefix='sdwan-path-selection-0002-sipuaresults')
        
        #####################
        # Apply test config #
        #####################
        logger.info("Applying test configuration")   
        stc.apply()

        #################################
        # Save STC configuration to xml #
        #################################
        logger.info('Saving STC configuration to XML file') 
        stc.perform('SaveAsXml', filename='path_selection_app_aware_steering.xml')

        #############################
        # Run commands in sequencer #
        #############################        
        ### Start the sequencer ###
        testState = 'PASSED'
        logger.info("Start sequencer...")   
        stc.perform('sequencerStart')

        ### Wait for sequencer to finish ###
        testState = stc.wait_until_complete()
        logger.info("Sequencer stopped")
        sequencerstatus = stc.get(sequencer, 'Status')
        
        ##############################
        # Get test result and return #
        ##############################        
        if testState != 'PASSED':
            errorinfo = 'Test failed, ' + sequencerstatus + '.\n'
            msgRobot = msgRobot + errorinfo
            self.stc.download_all_files(self.outdir)
            raise RuntimeError(errorinfo)
        else:
            msgRobot = msgRobot + 'Test Passed.\n'
        logger.info('Sequencer status is '+testState)
        return msgRobot
        
    def cleanup(self):
        if self.stc is not None:
            # Download everything #
            self.stc.download_all_files(self.outdir)

        super().cleanup()
