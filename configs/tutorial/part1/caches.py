## Configuration file for caches

import m5 # Import m5 library 
from m5.objects import Cache # Import the SimObject for the cache

## Create the L1 cache object by extending the BaseCache SimObject in src/mem/cache/Cache.py

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None): # Declare the constructor (__init__ functions in Python)
        super(L1Cache, self).__init__() # Always call the superclass's constructor
        pass
    
    def connectCPU(self, cpu): # Function to connect to a CPU
        # need to define this in a base class!
        raise NotImplementedError
    
    def connectBus(self, bus): # Function to connect to a bus
        self.mem_side = bus.cpu_side_ports

## Create the L1 caches sub-classes

class L1ICache(L1Cache):
    size = '16kB'

    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    size = '64kB'

    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

## Create the L2 with some reasonable parameters

class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports