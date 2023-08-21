#include "learning_gem5/part2/hello_object.hh"
#include "base/trace.hh"
#include "debug/HelloExample.hh" // Include the automatically generated header file as a new debug flag is added to configs/learning_gem5/part2/SConscript

#include <iostream>

namespace gem5
{
    HelloObject::HelloObject(const HelloObjectParams &params) : SimObject(params) // Pass the parameter object to the SimObject parent
    {
        //std::cout << "Hello World! From a SimObject" << std::endl; // Normally never use std::cout in gm5, instead use debug flags
        DPRINTF(HelloExample, "Created the hello object\n"); // Replacing the std::cout with the debug statememt (DPRINTF is a C++ macro)
    }
} // namespace gem5