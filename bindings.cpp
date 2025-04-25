#include <pybind11/pybind11.h>
#include "physics.h"

namespace py = pybind11;

PYBIND11_MODULE(physics, m) {
    m.def("check_collision", &check_collision, "Check collision between two circles");
}