## Extends the simple.py by adding a cache hierarchy (L1D$, L1I$, and unidifed L2$)
## Because we are using a single-core, we don't care about modeling cache coherence

import m5 # Import m5 library 
from m5.objects import * # Import all compiled SimObjects
from caches import * # Import the names from caches.py

## Import the argument parser library from Python
import argparse

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("binary", default="", nargs="?", type=str, help="Path to the binary to execute")
parser.add_argument("--l1i_size", help="L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", help="L1 data cache size. Default: 64kB.")
parser.add_argument("--l2_size",  help="L2 cache size. Default: 256 kB.")

options = parser.parse_args()
## Configure the System

system = System() # The System object will be the parent of all the other objects in the simulated system

system.clk_domain = SrcClockDomain() # Create a clock domain
system.clk_domain.clock = '1GHz'     # Set the clock to 1 GHz
system.clk_domain.voltage_domain = VoltageDomain() # Specify the voltage domain for this clock domain

## Set up memory. It will almost always be a timing model for the memory simulation

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')] # Single memory range of size 512 MB (very small system)

## Create the CPU. The fopllowing is the simplest timing-based CPu for x86. 
## This CPU executes each instruction in one clock, except memory requests, which flow through the memory system

system.cpu = X86TimingSimpleCPU()

## Create the L1 caches

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

## Connect the caches to the CPU ports through the helper functions we created

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

## Create an L2 bus to connect the L1 caches to the L2 cache (the L2 only expects one port)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

## Create the L2 and connect to the L2 bus and the memory bus

system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

## Create the system-wide memory bus

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

## Create the I/O controller on the CPU side and connect to the memory bus
## Connecting the PIO and interrupt ports to the memory bus is an x86-specific requirement. Other ISAs do not require these extra lines.

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

## Create the memory controller

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8() # Use a simple DDR3 controller responsible for the entire memory range of the system
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

## Provide the binary to execute and set up the process
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    "tests/test-progs/hello/bin/x86/linux/hello",
)

## for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)
## The following is needed to pass the binary through the parsed options
# system.workload = SEWorkload.init_compatible(options.binary)

## Create the process (a SimObject)

process = Process()
process.cmd = [binary] # Set the process command to the command we want to run
system.cpu.workload = process # Use the process as the CPU workload
system.cpu.createThreads() # Create the functional execution context

## Instantiate the system and begin execution

root = Root(full_system = False, system = system) # Create the Root object
m5.instantiate() # Instantiate the simulation

## Kick off the simulation

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}' .format(m5.curTick(), exit_event.getCause()))