import settings
import pickle as pkl
import numpy as np

# assert speedups:
for dimtype in settings.dimreduction_types:
    for d in settings.d_list:
        fname = settings.brute_force_fnames[dimtype][d]
        with open(fname, 'r') as f:
            bangles = np.array(pkl.load(f)['angles'])
        fname = settings.speedup_fnames[dimtype][d]
        with open(fname, 'r') as f:
            sangles = np.array(pkl.load(f)['angles'])
        correct = np.abs(bangles - sangles) < 10 ** -5
        if not correct.all():
            print "error with speedups", dimtype, d

# assert approximations:
for eps_i in range(2):
    onepluseps = settings.eps_list[eps_i]
    print onepluseps
    for dimtype in settings.dimreduction_types:
        for d in settings.d_list:
            fname = settings.brute_force_fnames[dimtype][d]
            with open(fname, 'r') as f:
                bangles = np.array(pkl.load(f)['angles'])
            fname = settings.approx_fnames[eps_i][dimtype][d]
            with open(fname, 'r') as f:
                aangles = np.array(pkl.load(f)['angles'])
            correct = bangles * onepluseps + 10 ** -5 > aangles
            if not correct.all():
                print "error with approx", dimtype, d
