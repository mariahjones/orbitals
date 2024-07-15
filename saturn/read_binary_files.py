def read_binary_files(filenames):
    '''
    reads binary files and extracts orbital elements from snapshots
    '''
    
    saturns_trojans = []
    for filename in filenames:
        sa = rebound.Simulationarchive(filename)

        tmax = sa.tmax
        tmin = sa.tmin
        nshots = len(sa)  # number of snapshots

        times = np.linspace(tmin, tmax, nshots)

        orbital_elements = []

        # Load in each snapshot
        for i in range(nshots):
            ps = sa[i].particles  # particles at snapshot i
            os = sa[i].orbits(primary=ps[0])  # orbits relative to the primary particle

            # Lists to hold orbital elements for the current snapshot
            a = []
            ecc = []
            inc = []
            omega = []
            Omega = []
            f = []
            mean_lon = []

            for j in range(len(os)):
                a.append(os[j].a)
                ecc.append(os[j].e)
                inc.append(np.degrees(os[j].inc))
                omega.append(os[j].omega)
                Omega.append(os[j].Omega)
                f.append(os[j].f)
                mean_lon.append(os[j].Omega + os[j].omega + os[j].l)

            # Append the lists of orbital elements for the current snapshot
            orbital_elements.append([a, ecc, inc, omega, Omega, f, mean_lon])

        # Append the times and orbital elements for all snapshots of the current file
        saturns_trojans.append((times, orbital_elements))
    return saturns_trojans