import settings

import matplotlib.pyplot as plt
import pickle as pkl

import numpy as np

""" This is a (simple) plotting script for the (exact) speedup results. """

fig_ll, ax_ll = plt.subplots()
fig_slx, ax_slx = plt.subplots()
fig_sly, ax_sly = plt.subplots()

for dimtype, symbol in zip(settings.dimreduction_types, "ods"):
    bf_runtimes = []
    su_runtimes = []
    for d in settings.d_list:
        fname = settings.brute_force_fnames[dimtype][d]
        with open(fname, 'r') as f:
            bf_runtimes.append(pkl.load(f)['time'])
        fname = settings.speedup_fnames[dimtype][d]
        with open(fname, 'r') as f:
            su_runtimes.append(pkl.load(f)['time'])
    speedups = bf_runtimes / np.array(su_runtimes)

    ax_ll.loglog(settings.d_list, speedups, marker=symbol, label=dimtype)
    ax_slx.semilogx(settings.d_list, speedups, marker=symbol, label=dimtype)
    ax_sly.semilogy(settings.d_list, speedups, marker=symbol, label=dimtype)


for ax in [ax_ll, ax_slx, ax_sly]:
    ax.legend(loc='best')
    ax.set_xlabel('$d$')
    ax.grid()
    ax.set_ylabel('Speedup')

for fig, axesstr in zip([fig_ll, fig_slx, fig_sly], ['loglog', 'semilogx', 'semilogy']):
    fig.savefig('../figs/speedups_' + axesstr + '.pdf')

# plt.show()
