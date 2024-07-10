import rebound
import numpy as np

sim = rebound.Simulation()
sim.integrator = "trace"
sim.dt = 0.0003
sim.save_to_file('kepler_80f.bin', interval=100,delete_file=True) # save as binary file

sol_mass = (2 * np.pi)**2 

jup_gm = 1.27E17 
jup_mass = (jup_gm / (1.33E20)) * sol_mass

star_mass = 0.73 * sol_mass

d_mass = 0.0212 * jup_mass
e_mass = 0.0130 * jup_mass
b_mass = 0.0218 * jup_mass
c_mass = 0.0212 * jup_mass

# calculate planet f mass proportions -- m1 = m2 * (r1/r2)^3

f_rad = 0.108 # in jupiter masses
d_rad = 0.136 # in jupiter masses

f_mass = d_mass * ((f_rad / d_rad) ** 3)

# add particles to the simulation

sim.add(m = star_mass, hash = 'Kepler-80')
sim.add(m = f_mass, a = 0.0175, inc = (90 - 86.50) * (np.pi/180), hash = 'Kepler-80f')
sim.add(m = d_mass, a = 0.0372, inc = (90 - 88.35) * (np.pi/180), hash = 'Kepler-80d')
sim.add(m = e_mass, a = 0.0491, inc = (90 - 88.79) * (np.pi/180), hash = 'Kepler-80e')
sim.add(m = b_mass, a = 0.0648, inc = (90 - 89.34) * (np.pi/180), hash = 'Kepler-80b')
sim.add(m = c_mass, a = 0.0792, inc = (90 - 89.33) * (np.pi/180), hash = 'Kepler-80c')

# add trojans
ps = sim.particles
os = sim.orbits()


#change for each sim
a_start = ps['Kepler-80f'].a
a_end = a_start * (1 + (f_mass / (3 * star_mass)) ** (1/3))

sem_maj_ax = np.linspace(a_start, a_end, 20)
#print(sem_maj_ax)

#eccs = [0.1, 0.08, 0.06, 0.04, 0.02, 0.]

#ecc = eccs[0]
omega = os[0].omega + (np.pi / 3)
inc = os[0].inc
Omega = os[0].Omega
f = os[0].f

for i in range(20):
    a = sem_maj_ax[i]
    hash_val = 'Trojan_1f_{}'.format(i)
    
    sim.add(a = a, inc = inc, omega = omega, Omega = Omega, f = f, hash = hash_val)

sim.N_active = 6 # number of active (non-massless) particles, sun and five planets

Nout = 10000 # number of points to display
tmax = 1000000 # let the simulation run for 80 years
Nplanets = 5

a = np.zeros((Nplanets,Nout))
#ecc = np.zeros((Nplanets,Nout))
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
        #ecc[j][i] = os[j].e
        Omega[j][i] = os[j].Omega
        omega[j][i] = os[j].omega
        inc[j][i] = os[j].inc
        f[j][i] = os[j].f
        
        # remove escaped particles
        #remove_indices = [i for i, orbit in enumerate(os) if orbit.a <= 0 or orbit.a >= 1]
        #for i in sorted(remove_indices, reverse=True):
            #sim.remove(i+1)