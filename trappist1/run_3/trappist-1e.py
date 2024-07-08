import rebound
import numpy as np

sim = rebound.Simulation()
sim.integrator = "trace"
sim.dt = 0.0003
sim.save_to_file('trappist_1e.bin', interval=1,delete_file=True) # save as binary file

sol_mass = (2 * np.pi)**2 

jup_gm = 1.27E17 
jup_mass = (jup_gm / (1.33E20)) * sol_mass

star_mass = 0.0898 * sol_mass

b_mass = 0.004323 * jup_mass

c_mass = 0.004115 * jup_mass

d_mass = 0.00122 * jup_mass

e_mass = 0.00218 * jup_mass

f_mass = 0.003269 * jup_mass

g_mass = 0.004156 * jup_mass

h_mass = 0.00103 * jup_mass

# add particles to the simulation (8)

sim.add(m = star_mass, hash = 'TRAPPIST-1')
sim.add(m = b_mass, a = 0.01154, inc = (90 - 89.728) * (np.pi/180), hash = 'TRAPPIST-1b')
sim.add(m = c_mass, a = 0.01580, inc = (90 - 89.778) * (np.pi/180), hash = 'TRAPPIST-1c')
sim.add(m = d_mass, a = 0.02227, inc = (90 - 89.896) * (np.pi/180), hash = 'TRAPPIST-1d')
sim.add(m = e_mass, a = 0.02925, inc = (90 - 89.793) * (np.pi/180), hash = 'TRAPPIST-1e')
sim.add(m = f_mass, a = 0.03849, inc = (90 - 89.740) * (np.pi/180), hash = 'TRAPPIST-1f')
sim.add(m = g_mass, a = 0.04683, inc = (90 - 89.742) * (np.pi/180), hash = 'TRAPPIST-1g')
sim.add(m = h_mass, a = 0.06189, inc = (90 - 89.805) * (np.pi/180), hash = 'TRAPPIST-1h')

# add trojans
ps = sim.particles
os = sim.orbits()


#change for each sim
a_start = ps['TRAPPIST-1e'].a
a_end = a_start * (1 + (e_mass / 3 * star_mass) ** 1/3)

sem_maj_ax = np.linspace(a_start, a_end, 20)
#print(sem_maj_ax)

#eccs = [0.1, 0.08, 0.06, 0.04, 0.02, 0.]

#ecc = eccs[0]
omega = os[3].omega + (np.pi / 3)
inc = os[3].inc
Omega = os[3].Omega
f = os[3].f

for i in range(20):
    a = sem_maj_ax[i]
    hash_val = 'Trojan_1e_{}'.format(i)
    
    sim.add(a = a, inc = inc, omega = omega, Omega = Omega, f = f, hash = hash_val)

sim.N_active = 8 # number of active (non-massless) particles, sun and seven planets

Nout = 10000 # number of points to display
tmax = 10000 # let the simulation run for 80 years
Nplanets = 7

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
        remove_indices = [i for i, orbit in enumerate(os) if orbit.a <= 0 or orbit.a >= 1]
        for i in sorted(remove_indices, reverse=True):
            sim.remove(i+1)


