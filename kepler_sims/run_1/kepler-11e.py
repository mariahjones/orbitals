import rebound
import numpy as np

sim = rebound.Simulation()
sim.integrator = "trace"
sim.dt = 0.001
sim.save_to_file('kepler_11e.bin', interval=10,delete_file=True) # save as binary file

sol_mass = (2 * np.pi)**2 

jup_gm = 1.27E17 
jup_mass = (jup_gm / (1.33E20)) * sol_mass

star_mass = 0.98600 * sol_mass

b_mass = 0.006 * jup_mass

c_mass = 0.009 * jup_mass

d_mass = 0.023 * jup_mass

e_mass = 0.025 * jup_mass

f_mass = 0.006 * jup_mass

g_mass = 0.078 * jup_mass


# add particles to the simulation

sim.add(m = star_mass, hash = 'Kepler-11')
sim.add(m = b_mass, a = 0.09223650991, hash = 'Kepler-11b')
sim.add(m = c_mass, a = 0.1078323443, hash = 'Kepler-11c')
sim.add(m = d_mass, a = 0.156105667, hash = 'Kepler-11d')
sim.add(m = e_mass, a = 0.1963171072, hash = 'Kepler-11e')
sim.add(m = f_mass, a = 0.2525546526, hash = 'Kepler-11f')
sim.add(m = g_mass, a = 0.4696205373, hash = 'Kepler-11g')

# add trojans
ps = sim.particles
os = sim.orbits()


#change for each sim
a_start = ps['Kepler-11e'].a
a_end = a_start * (1 + (e_mass / 3 * star_mass) ** 1/3)

sem_maj_ax = np.linspace(a_start, a_end, 20)
#print(sem_maj_ax)

#eccs = [0.1, 0.08, 0.06, 0.04, 0.02, 0.]

#ecc = eccs[0]
omega = os[3].omega + (np.pi / 3)
Omega = os[3].Omega
f = os[3].f

for i in range(20):
    a = sem_maj_ax[i]
    hash_val = 'coorb_11e_{}'.format(i)
    
    sim.add(a = a, omega = omega, Omega = Omega, f = f, hash = hash_val)

sim.N_active = 7 # number of active (non-massless) particles, sun and six planets

Nout = 10000 # number of points to display
tmax = 100000
Nplanets = 6

a = np.zeros((Nplanets,Nout))
#ecc = np.zeros((Nplanets,Nout))
Omega = np.zeros((Nplanets,Nout))
omega = np.zeros((Nplanets,Nout))
#inc = np.zeros((Nplanets, Nout))
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
        #inc[j][i] = os[j].inc
        f[j][i] = os[j].f
        
        # remove escaped particles
        #remove_indices = [i for i, orbit in enumerate(os) if orbit.a <= 0 or orbit.a >= 1]
        #for i in sorted(remove_indices, reverse=True):
        #    sim.remove(i+1)