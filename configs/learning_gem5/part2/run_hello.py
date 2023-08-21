# Configuration script for the learning-gem5/part2 tutorial

import m5
# Import all the compiled objects
from m5.objects import *

# Instantiate the Root object, required by all the gem5 instances
root = Root(full_system = False)

# Declare the object as a child of the root object. In this case, we call the constructor with no parameters
root.hello = HelloObject()
# Call instantiate on the m5 module and run the simulation
m5.instantiate()

print("Beginning Simulation")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))