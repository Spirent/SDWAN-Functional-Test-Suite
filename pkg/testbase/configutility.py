
class base_config():
    """
    It is base Class for parsing config parameters.

    """   
    def __init__(self, cfg):
        if cfg == None:
           raise RuntimeError("Config object is None")

    def getValue(self, dictTemp, keyList):
        for key in keyList:
            if key in dictTemp:
                dictTemp = dictTemp[key]
            else:
                return ('')
        return dictTemp

class sne_config(base_config):
    """
    Sne config Class for parsing SNE config parameters
    """
    def __init__(self, cfg):
        super().__init__(cfg)
        #Disruptor
        self.disruptorDelay = self.getValue(cfg,['Disruptor','PacketDelayDisruptor','Delay'])
        self.disruptorJitter = self.getValue(cfg,['Disruptor','PacketDelayDisruptor','Jitter'])
        self.disruptorDuration = self.getValue(cfg,['Disruptor','PacketDelayDisruptor','Duration'])
        self.disruptorMaxThroughput = self.getValue(cfg,['Disruptor','PacketDelayDisruptor','MaxThroughput'])

        #Corruptor
        self.corruptorPacketDropCount = self.getValue(cfg,['Corruptor','PacketDropCorruptor','PerPacketCount'])
        self.corruptorDuration = self.getValue(cfg,['Corruptor','PacketDropCorruptor','Duration'])
        self.corruptorPerPacketCount = self.getValue(cfg,['Corruptor','PacketDropCorruptor','PerPacketCount'])
