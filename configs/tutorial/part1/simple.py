import m5
from m5.objects import *
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]
# system.cpu = X86TimingSimpleCPU()
system.cpu = ArmTimingSimpleCPU()
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports # Request port = Response port
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.createInterruptController()
# system.cpu.interrupts[0].pio = system.membus.mem_side_ports # Specific to X86
# system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports # Specific to X86
# system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports # Specific to X86

system.system_port = system.membus.cpu_side_ports
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    # "tests/test-progs/hello/bin/x86/linux/hello", # Hello world binary for the X86 model
    "cpu_tests/benchmarks/bin/arm/Bubblesort",
)

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)
m5.instantiate()
print("Beginning Simulation")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}' .format(m5.curTick(), exit_event.getCause()))
