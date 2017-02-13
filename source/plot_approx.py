import settings

import matplotlib.pyplot as plt
import pickle as pkl

import numpy as np

""" This is a (simple) plotting script for the approximative algorithm. """

for eps_i in range(0, 2):
    eps = settings.eps_list[eps_i]
    print eps
    fig_ll, ax_ll = plt.subplots()
    fig_slx, ax_slx = plt.subplots()
    fig_sly, ax_sly = plt.subplots()

    fige_ll, axe_ll = plt.subplots()
    fige_slx, axe_slx = plt.subplots()
    fige_sly, axe_sly = plt.subplots()

    for dimtype, symbol in zip(settings.dimreduction_types, "ods"):
        bf_runtimes = []
        approx_runtimes = []
        approx_errs = []

        for d in settings.d_list:
            fname = settings.brute_force_fnames[dimtype][d]
            with open(fname, 'r') as f:
                data = pkl.load(f)
                bf_runtimes.append(data['time'])
                bangles = np.array(data['angles'])
                bf_tweets = np.array(data['tweet_indices'])

            # try:
            fname = settings.approx_fnames[eps_i][dimtype][d]
            with open(fname, 'r') as f:
                data = pkl.load(f)
                approx_runtimes.append(data['time'])
                aangles = np.array(data['angles'])
                approx_tweets = np.array(data['tweet_indices'])

            zeros = aangles < 10 ** -4
            errs = (aangles - bangles) / bangles
            errs[zeros] = 0
            approx_errs.append(np.mean(errs))

        speedups = bf_runtimes / np.array(approx_runtimes)
        print eps

        ax_ll.loglog(
            settings.d_list, speedups, marker=symbol, label=dimtype)
        ax_slx.semilogx(
            settings.d_list, speedups, marker=symbol, label=dimtype)
        ax_sly.semilogy(
            settings.d_list, speedups, marker=symbol, label=dimtype)

        axe_ll.semilogx(
            settings.d_list, approx_errs, marker=symbol, label=dimtype)
        axe_slx.semilogx(
            settings.d_list, approx_errs, marker=symbol, label=dimtype)
        axe_sly.semilogx(
            settings.d_list, approx_errs, marker=symbol, label=dimtype)

    for ax in [ax_ll, ax_slx, ax_sly]:
        ax.legend(loc='best')
        ax.set_xlabel('$d$')
        ax.grid()
        ax.set_ylabel('Speedup')
        if ax == ax_ll:
            ax.set_ylim(10 ** -2, 10 ** 2)

    for ax in [axe_ll, axe_slx, axe_sly]:
        ax.legend(loc='best')
        ax.set_xlabel('$d$')
        ax.grid()
        ax.set_ylabel('Mean approximation error')

    for fig, axesstr in zip([fig_ll, fig_slx, fig_sly], ['loglog', 'semilogx', 'semilogy']):
        fig.suptitle('approximate speedup, eps=' + str(eps - 1) + ".pdf")
        fig.savefig(
            '../figs/speedups_approx_' + str(eps) + "_" + axesstr + '.pdf')

    for fig, axesstr in zip([fige_ll, fige_slx, fige_sly], ['loglog', 'semilogx', 'semilogy']):
        fig.suptitle('approximation error, eps ' + str(eps - 1) + ".pdf")
        fig.savefig(
            '../figs/approximation_error_eps_' + str(eps) + "_" + axesstr + '.pdf')

# plt.show()
