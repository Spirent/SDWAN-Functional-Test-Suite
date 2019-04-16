
class stc_config_sdwan():
    """
    Config STC class for parsing parameters.

    """   
    def __init__(self, cfg):
        DEVICENUMBER = 10
        STREAMNUMBER = 10
        #Use exec to create multiple objects.
        for i in range(1,DEVICENUMBER):
            exec("self.ipDevice{0} = self.getValue(cfg, ['EmulatedDevice','EmulatedDevice{1}','Ipv4If','Address'])".format(i, i))
            exec("self.gatewayDevice{0} = self.getValue(cfg, ['EmulatedDevice','EmulatedDevice{1}','Ipv4If','Gateway'])".format(i, i))
            exec("self.nameDevice{0} = self.getValue(cfg, ['EmulatedDevice','EmulatedDevice{1}','Name'])".format(i, i))
            exec("self.countDevice{0} = self.getValue(cfg, ['EmulatedDevice','EmulatedDevice{1}','DeviceCount'])".format(i, i))
        for i in range(1,STREAMNUMBER):
            exec("self.nameStream{0} = self.getValue(cfg, ['StreamBlock','StreamBlock{1}','Name'])".format(i, i))
            exec("self.frameLengthMode{0} = self.getValue(cfg, ['StreamBlock', 'StreamBlock{1}', 'FrameLengthMode'])".format(i, i))
            exec("self.fixedFrameLength{0} = self.getValue(cfg, ['StreamBlock', 'StreamBlock{1}', 'FixedFrameLength'])".format(i, i))
            exec("self.frameLengthDistribution{0} = self.getValue(cfg, ['StreamBlock', 'StreamBlock{1}', 'FrameLengthDistribution', 'Name'])".format(i, i))
            exec("self.frameConfigStream{0} = self.getValue(cfg, ['StreamBlock','StreamBlock{1}','FrameConfig'])".format(i, i))
            exec("self.rangeModifierStream{0} = self.getValue(cfg, ['StreamBlock','StreamBlock{1}','RangeModifier'])".format(i, i))

        self.namePort = self.getValue(cfg, ['Name'])
        self.ifCountDevice = self.getValue(cfg, ['ifCount'])
        self.ifStackDevice = self.getValue(cfg, ['ifStack'])
        self.linkTypeDevice = self.getValue(cfg, ['LinkType'])
        self.frameLength = self.getValue(cfg, ['frameLength'])
        self.loadUnitPort = self.getValue(cfg, ['GeneratorConfig','LoadUnit'])
        self.fixedLoadPort = self.getValue(cfg, ['GeneratorConfig','FixedLoad'])
        self.waitTimeAfterDisableSne = self.getValue(cfg, ['waitTimeAfterDisableSne'])
        self.waitTimeAfterBreakLink = self.getValue(cfg, ['waitTimeAfterBreakLink'])
        self.waitIntervalAfterBreakLink = self.getValue(cfg, ['waitIntervalAfterBreakLink'])
        self.waitTimeAfterRecoverLink = self.getValue(cfg, ['waitTimeAfterRecoverLink'])
        self.waitIntervalAfterRecoverLink = self.getValue(cfg, ['waitIntervalAfterRecoverLink'])
        self.schedulingMode = self.getValue(cfg, ['GeneratorConfig', 'SchedulingMode'])
        self.durationMode = self.getValue(cfg, ['GeneratorConfig', 'DurationMode'])
        self.duration = self.getValue(cfg, ['GeneratorConfig', 'Duration'])
        self.loadUnitStream = self.getValue(cfg, ['LoadUnit'])
        self.loadStream = self.getValue(cfg, ['Load'])

    def getValue(self, dictTemp, keyList):
        for key in keyList:
            if key in dictTemp:
                dictTemp = dictTemp[key]
            else:
                return ('')
        return dictTemp
