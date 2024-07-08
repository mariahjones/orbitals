# Hypothetical Trojans of Saturn
import rebound
import numpy as np
#import pandas as pd

#%matplotlib inline
#import matplotlib.pyplot as plt

sim = rebound.Simulation()
sim.integrator = "trace"
#sim.dt = 1
sim.save_to_file('saturn_troj5.bin', interval=1e4,delete_file=True) # save as binary file

# Convert au/days to au/years
vel_x = [0.0, -6.584186332911239E-03,1.361833139322700E-03, -3.176609453266956E-03, 1.106505958060795E-04]
vel_y = [0.0, 4.208054867943963E-03, 5.314892732297496E-03, 2.188750863994737E-03, 3.160539398425530E-03]
vel_z = [0.0, 1.298323287693746E-04, -1.466946539551684E-04, 4.926573452085599E-05, -6.757068282993264E-05]

vel_x = np.array(vel_x) * 365.25636
vel_y = np.array(vel_y) * 365.25636
vel_z = np.array(vel_z) * 365.25636


# Convert mass to integration units
sol_mass = (2 * np.pi)**2 # integration units
sol_gm = (1.33E20) # real units

jup_gm = 1.27E17 
jup_mass = (jup_gm / sol_gm) * sol_mass


sat_gm = 3.79E16
sat_mass = (sat_gm / sol_gm) * sol_mass

ur_gm = 5.79E15 
ur_mass = (ur_gm / sol_gm) * sol_mass

nep_gm = 6.84E15
nep_mass = (nep_gm / sol_gm) * sol_mass


# add particles to the simulation

sim.add(m = sol_mass, x = 0, y = 0, z = 0,
        vx = vel_x[0], vy = vel_y[0], vz = vel_z[0], hash = 'Sun')
sim.add(m = jup_mass, x = 2.559959519433896E+00, y = 4.317254861986015E+00, z =-7.520814690745442E-02,
        vx= vel_x[1], vy= vel_y[1], vz= vel_z[1], hash = 'Jupiter')
sim.add(m = sat_mass, x = 9.241056053800349E+00, y =-2.909785985421069E+00, z =-3.171865429820031E-01,
        vx= vel_x[2], vy= vel_y[2], vz= vel_z[2], hash = 'Saturn')
sim.add(m = ur_mass, x = 1.178746554190535E+01, y = 1.564471912991385E+01, z =-9.472686043780910E-02,
        vx= vel_x[3], vy= vel_y[3], vz= vel_z[3], hash = 'Uranus')
sim.add(m = nep_mass, x = 2.986403735565160E+01, y =-1.304275085444185E+00, z =-6.613439117521470E-01,
        vx= vel_x[4], vy= vel_y[4], vz= vel_z[4], hash = 'Neptune')


ps = sim.particles
os = sim.orbits()


a_start = os[1].a
a_end = a_start * (1 + (sat_mass / 3 * sol_mass) ** 1/3)

sem_maj_ax = np.linspace(a_start, a_end, 20)
#print(sem_maj_ax)

eccs = [0.1, 0.08, 0.06, 0.04, 0.02, 0.]

ecc = eccs[5]
omega = os[1].omega + (np.pi / 3)
inc = os[1].inc
Omega = os[1].Omega
f = os[1].f

for i in range(20):
    a = sem_maj_ax[i]
    
    sim.add(a = a, e = ecc, inc = inc, omega = omega, Omega = Omega, f = f)

sim.N_active = 5 # number of active particles, sun and four giants

Nout = 10000  # number of points to display, corresponding to 10^4 years
tmax = 100000000  # run the simulation for 10^8 years

times = np.linspace(0., tmax, Nout)

for time in times:
    sim.integrate(time)
    os = sim.orbits()  # Update os with the latest orbits
    remove_indices = [i for i, orbit in enumerate(os) if orbit.a <= 0]
    for i in sorted(remove_indices, reverse=True):
        sim.remove(i+1)