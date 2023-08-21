from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    type = 'HelloObject' # Type should not be strictly the class type, but it is convention. It is the C++ class that we are wrapping with this Python SimObject
    cxx_header = "learning_gem5/part2/hello_object.hh" # It is the file that contains thwe declaration of the class used as the type parameter
    cxx_class = "gem5::HelloObject" # The newly created SimObject is declared within the gem5 namespace