import settings
import matplotlib.pyplot as plt
import pickle as pkl

""" This is a (simple) plotting script for the brute force results. """

fig_ll, ax_ll = plt.subplots()
fig_slx, ax_slx = plt.subplots()
fig_sly, ax_sly = plt.subplots()

for dimtype, symbol in zip(settings.dimreduction_types, "ods"):
    runtimes = []
    for d in settings.d_list:
        fname = settings.brute_force_fnames[dimtype][d]
        with open(fname, 'r') as f:
            runtimes.append(pkl.load(f)['time'])
    ax_ll.loglog(settings.d_list, runtimes, marker=symbol, label=dimtype)
    ax_slx.semilogx(settings.d_list, runtimes, marker=symbol, label=dimtype)
    ax_sly.semilogy(settings.d_list, runtimes, marker=symbol, label=dimtype)

for ax in [ax_ll, ax_slx, ax_sly]:
    ax.legend(loc='best')
    ax.set_xlabel('$d$')
    ax.grid()
    ax.set_ylabel('Running time (in seconds)')

for fig, axesstr in zip([fig_ll, fig_slx, fig_sly], ['loglog', 'semilogx', 'semilogy']):
    fig.savefig('../figs/brute_force_runtimes_' + axesstr + '.pdf')

# plt.show()
