#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "ising.hpp"

namespace py = pybind11;

PYBIND11_MODULE(ising_cpp, m){
	py::class_<Ising>(m, "Ising")
		// initializing
		.def(py::init<unsigned int, bool>(),
			py::arg("L"), py::arg("init") = true)
		// properties
		.def_property_readonly("L", &Ising::get_L, "Site length of the system")
		.def_property_readonly("L2", &Ising::get_L2, "Number of spins in the system (L*L)")
		.def_property("lattice", &Ising::get_lattice, &Ising::set_lattice, "A 1D representation of the system")
		.def_property_readonly("energy", &Ising::energy, "Total energy of the system")
		.def_property_readonly("magnetization", &Ising::magnetization, "Magnetization of the system")
		// getter and setter
		.def("set_spin", &Ising::set_spin, "Setting the spin at position i,j",
			py::arg("i"), py::arg("j"), py::arg("value"))
		.def("get_spin", &Ising::get_spin, "Getting spin at position i,j",
			py::arg("i"), py::arg("j"))
		.def("flip_spin", &Ising::flip_spin, "Flipping spin at position i,j",
			py::arg("i"), py::arg("j"))
		// methods and functions
		.def("_local_energy", &Ising::local_energy, "Local energy at position i,j",
			py::arg("i"), py::arg("j"))
		;
}