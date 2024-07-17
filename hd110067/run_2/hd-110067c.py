import rebound
import numpy as np

sim = rebound.Simulation()
sim.integrator = "trace"
sim.dt = 0.001
sim.save_to_file('hd_c.bin', interval=10,delete_file=True) # save as binary file

sol_mass = (2 * np.pi)**2 

jup_gm = 1.27E17 
jup_mass = (jup_gm / (1.33E20)) * sol_mass

star_mass = 0.798 * sol_mass
b_mass = 0.0179 * jup_mass
c_mass = 0.020 * jup_mass
d_mass = 0.02681 * jup_mass
e_mass = 0.012 * jup_mass
f_mass = 0.0159 * jup_mass
g_mass = 0.026 * jup_mass


# add particles to the simulation

sim.add(m = star_mass, hash = 'HD-110067')
sim.add(m = b_mass, a = 0.07930, inc = (90 - 89.061) * (np.pi/180), hash = 'HD-110067b')
sim.add(m = c_mass, a = 0.1039, inc = (90 - 89.687) * (np.pi/180), hash = 'HD-110067c')
sim.add(m = d_mass, a = 0.1362, inc = (90 - 89.248) * (np.pi/180), hash = 'HD-110067d')
sim.add(m = e_mass, a = 0.1785, inc = (90 - 89.867) * (np.pi/180), hash = 'HD-110067e')
sim.add(m = f_mass, a = 0.2163, inc = (90 - 89.673) * (np.pi/180), hash = 'HD-110067f')
sim.add(m = g_mass, a = 0.2621, inc = (90 - 89.729) * (np.pi/180), hash = 'HD-110067g')

# add trojans
ps = sim.particles
os = sim.orbits()

#change for each sim
a_start = ps['HD-110067c'].a
a_end = a_start * (1 + (c_mass / (3 * star_mass)) ** (1/3))

sem_maj_ax = np.linspace(a_start, a_end, 20)

omega = os[1].omega + (np.pi / 3)
inc = os[1].inc
Omega = os[1].Omega
f = os[1].f

for i in range(20):
    a = sem_maj_ax[i]
    hash_val = 'Trojan_110067c_{}'.format(i)
    
    sim.add(a = a, inc = inc, omega = omega, Omega = Omega, f = f, hash = hash_val)

sim.N_active = 7 # number of active (non-massless) particles, sun and six planets

Nout = 10000 # number of points to display
tmax = 100000 # let the simulation run for 10^5 years
Nplanets = 6

a = np.zeros((Nplanets,Nout))
Omega = np.zeros((Nplanets,Nout))
omega = np.zeros((Nplanets,Nout))
inc = np.zeros((Nplanets, Nout))
f = np.zeros((Nplanets, Nout))

times = np.linspace(0.,tmax,Nout)
ps = sim.particles

for i,time in enumerate(times):
    sim.integrate(time)
    os = sim.orbits()
    for j in range(Nplanets):
        a[j][i] = os[j].a 
        Omega[j][i] = os[j].Omega
        omega[j][i] = os[j].omega
        inc[j][i] = os[j].inc
        f[j][i] = os[j].f