#ifndef __LEARNING_GEM5_HELLO_OBJECT_HH__
#define __LEARNING_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

namespace gem5 // The class is declared within the gem5 namespace scope
{
    class HelloObject : public SimObject // Inherits from the C++ SimObject class
    {
        public:
            HelloObject(const HelloObjectParams &p); // The constructor takes a parameter object. The parameter object is automatically created by the build system
    };                                               // from the name of our object (in this case, "HelloObject")
} // namespace gem5

#endif // __LEARNING_GEM5_HELLO_OBJECT_HH__