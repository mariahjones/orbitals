import rebound
import numpy as np

sim = rebound.Simulation()
sim.integrator = "trace"
sim.dt = 0.001
sim.save_to_file('kepler_90f.bin', interval=10,delete_file=True) # save as binary file

sol_mass = (2 * np.pi)**2 

gm_earth = (398600.435507) * (10 ** 9)
m_earth = (gm_earth / (1.33E20)) * sol_mass

star_mass = 1.1080 * sol_mass

# ratio of planet radius to earth radius (R / R_earth)

b_rat = 1.3
c_rat = 1.445
i_rat = 1.32
d_rat = 2.866
e_rat = 2.612
f_rat = 2.77
g_rat = 7.718
h_rat = 11.252

# calculate mass using proportions -- m = m_earth * (R/R_earth)^2.01

b_mass = m_earth * ((b_rat)**2.01)
c_mass = m_earth * ((c_rat)**2.01)
i_mass = m_earth * ((i_rat)**2.01)
d_mass = m_earth * ((d_rat)**2.01)
e_mass = m_earth * ((e_rat)**2.01)
f_mass = m_earth * ((f_rat)**2.01)
g_mass = m_earth * ((g_rat)**2.01)
h_mass = m_earth * ((h_rat)**2.01)

# add particles to the simulation

sim.add(m = star_mass, hash = 'Kepler-90')
sim.add(m = b_mass, a = 0.07416416275, hash = 'Kepler-90b')
sim.add(m = c_mass, a = 0.08579429312, hash = 'Kepler-90c')
sim.add(m = i_mass, a = 0.1201380843, hash = 'Kepler-90i')
sim.add(m = d_mass, a = 0.309467855, hash = 'Kepler-90d')
sim.add(m = e_mass, a = 0.412531915, hash = 'Kepler-90e')
sim.add(m = f_mass, a = 0.5060567991, hash = 'Kepler-90f')


# add trojans
ps = sim.particles
os = sim.orbits()

#change for each sim
a_start = ps['Kepler-90f'].a
a_end = a_start * (1 + (f_mass / (3 * star_mass)) ** (1/3))

sem_maj_ax = np.linspace(a_start, a_end, 20)

omega = os[5].omega + (np.pi / 3)
inc = os[5].inc
Omega = os[5].Omega
f = os[5].f

for i in range(20):
    a = sem_maj_ax[i]
    hash_val = 'Trojan_90f_{}'.format(i)
    
    sim.add(a = a, inc = inc, omega = omega, Omega = Omega, f = f, hash = hash_val)

sim.add(m = g_mass, a = 0.7168522035, hash = 'Kepler-90g')
sim.add(m = h_mass, a = 0.9702055452, hash = 'Kepler-90h')

sim.N_active = 9 # number of active (non-massless) particles, sun and eight planets

Nout = 10000 # number of points to display
tmax = 100000 # let the simulation run for 80 years
Nplanets = 8

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