#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "ising.hpp"

#define STRINGIFY(x) #x


namespace py = pybind11;

PYBIND11_MODULE(__ising, m){
#ifdef VERSION_INFO
	m.attr("__version__") = STRINGIFY(VERSION_INFO);
#else
	m.attr("__version__") = "dev";
#endif

	py::class_<Ising>(m, "Ising")
		// initializing
		.def(py::init<unsigned int, bool>(),
			py::arg("L"), py::arg("init") = true)
		.def("randomize", &Ising::randomize, "Setting all spin to random values")
		// properties
		.def_property_readonly("L", &Ising::get_L, "Site length of the system")
		.def_property_readonly("L2", &Ising::get_L2, "Number of spins in the system (L*L)")
		.def_property("lattice", &Ising::get_lattice, &Ising::set_lattice, "A 1D representation of the system")
		.def_property_readonly("energy", &Ising::energy, "Total energy of the system")
		.def_property_readonly("magnetization", &Ising::magnetization, "Magnetization of the system")
		// getters and setters
		.def("set_spin_by_index", &Ising::set_spin_by_index, "Setting the spin at position i,j",
			py::arg("index"), py::arg("value"))
		.def("get_spin_by_index", &Ising::get_spin_by_index, "Getting spin at position i,j",
			py::arg("index"))
		.def("set_spin", &Ising::set_spin, "Setting the spin at position i,j",
			py::arg("i"), py::arg("j"), py::arg("value"))
		.def("get_spin", &Ising::get_spin, "Getting spin at position i,j",
			py::arg("i"), py::arg("j"))
		.def("flip_spin", &Ising::flip_spin, "Flipping spin at position i,j",
			py::arg("i"), py::arg("j"))
		// methods and functions
		.def("_local_energy", &Ising::local_energy, "Local energy at position i,j",
			py::arg("i"), py::arg("j"))
		// simulate
		.def("metropolis", &Ising::metropolis, "Calculate n metropolis steps and return acceptance rate, <e>, <|mu|>",
			py::arg("steps"), py::arg("beta") = 0.0)
		;
}
