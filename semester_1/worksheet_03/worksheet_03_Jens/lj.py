#!/usr/bin/env python3
#from numba import njit, prange
import itertools
# introduce classes to the students
class Simulation:
    def __init__(self, dt, x, v, box, r_cut, shift,FMAX=None):
        self.dt = dt
        self.x = x.copy()
        self.v = v.copy()
        self.box = box.copy()
        self.r_cut = r_cut
        self.shift = shift

        self.n_dims = self.x.shape[0]
        self.n = self.x.shape[1]
        self.f = np.zeros_like(x)
        self.FMAX = FMAX
        self.warmup = True

        # both r_ij_matrix and f_ij_matrix are computed in self.forces()
        self.r_ij_matrix = np.zeros((self.n, self.n, self.n_dims))
        self.f_ij_matrix = np.zeros((self.n, self.n, self.n_dims))
        # computed in e_pot_ij_matrix
        self.e_pot_ij_matrix = np.zeros((self.n, self.n))

    
    def distances(self):
        self.r_ij_matrix = np.repeat([self.x.transpose()], self.n, axis=0)
        self.r_ij_matrix -= np.transpose(self.r_ij_matrix, axes=[1, 0, 2])
        # minimum image convention
        image_offsets = self.r_ij_matrix.copy()
        for nth_box_component, box_component in enumerate(self.box):
            image_offsets[:, :, nth_box_component] = \
                np.rint(image_offsets[:, :, nth_box_component] / box_component) * box_component
        self.r_ij_matrix -= image_offsets


    def energies(self):
        r = np.linalg.norm(self.r_ij_matrix, axis=2)
        with np.errstate(all='ignore'):
            self.e_pot_ij_matrix = np.where((r != 0.0) & (r < self.r_cut),
                                            4.0 * (np.power(r, -12.) - np.power(r, -6.)) + self.shift, 0.0)
        
    def kinetic_energy(self):
        return 0.5*sum(sum(self.v*self.v))
    
    def forces(self):
        # first update the distance vector matrix, obeying minimum image convention
        self.distances()
        self.f_ij_matrix = self.r_ij_matrix.copy()
        r = np.linalg.norm(self.r_ij_matrix, axis=2)
        with np.errstate(all='ignore'):
            fac = np.where((r != 0.0) & (r < self.r_cut),
                           4.0 * (12.0 * np.power(r, -13.) - 6.0 * np.power(r, -7.)), 0.0)
        for dim in range(self.n_dims): # numba
            with np.errstate(invalid='ignore'):
                self.f_ij_matrix[:, :, dim] *= np.where(r != 0.0, fac / r, 0.0)
        #FMAX = 0
        #if Fmax != 0:
            #self.f_ij_matrix[self.f_ij_matrix > FMAX] = FMAX
        #for i in range(1,self.n):
        #    for j in range(1,self.n):
        #        abs = scipy.linalg.norm(self.f_ij_matrix)
        #        if abs > FMAX:
        #            self.f_ij_matrix[i, j] =  self.f_ij_matrix[i,j]/abs * FMAX
        self.f = np.sum(self.f_ij_matrix, axis=0).transpose()
        if self.FMAX and self.warmup:
            capped = []
            for i in range(0,len(self.f)):
                abs_ = scipy.linalg.norm(self.f)
                capped.append(abs_ > self.FMAX)
                if capped[-1]:
                    self.f[i] = self.f[i]/abs_ * self.FMAX
            self.warmup = any(capped)
                    



        


    def energy(self):
        """Compute and return the energy components of the system."""
        # compute energy matrix
        self.energies()
        e_kin = self.kinetic_energy()
        e_pot = sum(itertools.chain(*self.e_pot_ij_matrix))
        return e_kin,e_pot
        

    
    def temperature(self):
        k=1
        e_kin=self.kinetic_energy()
        Temp = 2/k *e_kin/(self.n*self.n_dims)
        return Temp

    
    def pressure(self):
        e_kin = self.kinetic_energy()
        
        force_part = 0
        for i in range(1, self.n):
            for j in range(i):
                f_ij = self.f_ij_matrix[i, j]
                r_ij = self.r_ij_matrix[i, j]
                force_part += np.dot(f_ij, r_ij)
        
        A = np.prod(self.box)
        return (e_kin + 0.5*force_part)/A

    def rdf(self):
        #TODO
        pass

    def propagate(self):
        # update positions
        self.x += self.v * self.dt + 0.5 * self.f * self.dt * self.dt

        # half update of the velocity
        self.v += 0.5 * self.f * self.dt

        # compute new forces
        self.forces()
        # we assume that all particles have a mass of unity

        # second half update of the velocity
        self.v += 0.5 * self.f * self.dt


def write_checkpoint(state, path, overwrite=False):
    if os.path.exists(path) and not overwrite:
        raise RuntimeError("Checkpoint file already exists")
    with open(path, 'wb') as fp:
        pickle.dump(state, fp)


if __name__ == "__main__":
    import argparse
    import pickle
    import logging

    import os.path

    import numpy as np
    import scipy.spatial  # todo: probably remove in template
    import tqdm

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'N_per_side',
        type=int,
        help='Number of particles per lattice side.')
    parser.add_argument(
        '--cpt',
        type=str,
        help='Path to checkpoint.')
    parser.add_argument(
        '--FMAX',
        type=float,
        help='Maximum Force during Warmup.')
    args = parser.parse_args()

    np.random.seed(2)

    DT = 0.01
    T_MAX = 1000.0
    N_TIME_STEPS = int(T_MAX / DT)

    R_CUT = 2.5
    SHIFT = 0.016316891136

    DIM = 2
    DENSITY = 0.316
    N_PER_SIDE = args.N_per_side
    N_PART = N_PER_SIDE**DIM
    VOLUME = N_PART / DENSITY
    BOX = np.ones(DIM) * VOLUME**(1. / DIM)

    SAMPLING_STRIDE = 3
    FMAX = args.FMAX
   

    if not args.cpt or not os.path.exists(args.cpt):
        logging.info("Starting from scratch.")
        # particle positions
        #x = np.array(list(itertools.product(np.linspace(0, BOX[0], N_PER_SIDE, endpoint=False),
                                            #np.linspace(0, BOX[1], N_PER_SIDE, endpoint=False)))).T
        x = (BOX * np.random.random((N_PART, DIM))).T

        # random particle velocities
        v = 0.5*(2.0 * np.random.random((DIM, N_PART)) - 1.0)

        positions = []
        energies = []
        pressures = []
        temperatures = []
        rdfs = []
    elif args.cpt and os.path.exists(args.cpt):
        logging.info("Reading state from checkpoint.")
        with open(args.cpt, 'rb') as fp:
            data = pickle.load(fp)

    sim = Simulation(DT, x, v, BOX, R_CUT, SHIFT, FMAX)

    # If checkpoint is used, also the forces have to be reloaded!
    if args.cpt and os.path.exists(args.cpt):
        sim.f = f

    print("Beginning Warmup")
    counter = 0
    while sim.warmup and args.FMAX:
        sim.propagate()
        if counter % SAMPLING_STRIDE == 0:
            sim.FMAX = sim.FMAX * 1.1
        counter += 1
    print("Warmup finished")

    for i in tqdm.tqdm(range(N_TIME_STEPS)):
        sim.propagate()

        if i % SAMPLING_STRIDE == 0:
            positions.append(sim.x.copy())
            pressures.append(sim.pressure())
            energies.append(np.sum(sim.energy()))
            temperatures.append(sim.temperature())
            rdfs.append(sim.rdf())
            

    if args.cpt:
        state = {
            'dt': DT, # saving for convenience
            'sampling_stride': SAMPLING_STRIDE, # saving for convenience
            'energies': energies,
            'positions': positions,
            'pressures': pressures,
            'temperatures': temperatures,
            'rdfs': rdfs,
            'LastV': sim.v
            }
        write_checkpoint(state, args.cpt, overwrite=True)
