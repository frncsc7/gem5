## Simple "Hello World" configuration script

import m5 # Import m5 library 
from m5.objects import * # Import all compiled SimObjects

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

## Create the system-wide memory bus

system.membus = SystemXBar()

## Connect the cache ports on the CPU to the memory bnus (in this example the system does not have any cache)

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

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