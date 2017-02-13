import os
from os import path
from collections import Counter
import numpy as np
from scipy.stats import binned_statistic
import matplotlib.pyplot as plt
import cPickle as pkl

import settings


def assert_tweets_are_sets():
    """
    Checks whether all the tweets are just sets.
    """
    with open(settings.tweets_data_fname, 'r') as f:
        line = f.readline()
        i = 0  # just for a verbose output
        while line:
            c = Counter(line.split())
            for elem, cnt in c.items():
                assert cnt == 1
            line = f.readline()
            # for verbose output
            i += 1
            if i % (settings.ntweets / 100) == 0:
                print float(i) / settings.ntweets


def plot_ccdf(ax, values):
    values = np.array(values)
    unique_values = np.unique(values)
    ccdf = np.zeros(len(unique_values))
    for i, x in enumerate(unique_values):
        ccdf[i] = np.sum(values >= x) / float(len(values))
    ax.loglog(unique_values, ccdf)


def compute_term_counts():
    c = Counter()
    with open(settings.tweets_data_fname, 'r') as f:
        line = f.readline()
        i = 0
        while line:
            c.update(line.split())
            # for verbose output
            i += 1
            if i % (settings.ntweets / 100) == 0:
                print float(i) / settings.ntweets
            line = f.readline()
    with open(settings.counter_fname, 'w') as f2:
        # the whole container stored for later use:
        pkl.dump(c, f2)


def compute_number_of_tweets_and_plot(recompute=False):
    """Compute how many times a term appears in a tweet"""
    # recompute counts only if required:
    if recompute or not path.exists(settings.counter_fname):
        compute_term_counts()

    # load data:
    with open(settings.counter_fname, "r") as f2:
        c = pkl.load(f2)
        counts = np.array(c.values())
        sorted_counts = np.sort(counts)

    # plot the orig distribution
    fig, ax = plt.subplots()
    c = Counter(sorted_counts)
    keys = c.keys()
    vals = c.values()
    ax.loglog(keys, vals, ".")
    ax.set_xlabel(r'Number of apparances $k$')
    ax.set_ylabel(r'$t_k$')
    fig.savefig('../figs/prepro_counts.pdf')

    # plot a binned distribution
    fig, ax = plt.subplots()
    bins = np.logspace(0, 7, 50)

    # computing bin centers
    centers, _, _ = binned_statistic(
        sorted_counts, sorted_counts, statistic='mean', bins=bins)

    # values
    vals, _ = np.histogram(sorted_counts, bins, density=True)
    ax.loglog(centers, vals)
    ax.set_xlabel(r'Number of apparances $k$')
    ax.set_ylabel(r'Probability density $P(k)$')
    ax.grid()
    fig.savefig('../figs/prepro_prob_density.pdf')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    print sorted_counts[:10]

    plot_ccdf(ax, sorted_counts)
    # ax.loglog(sorted_counts, np.linspace(
    #     1, 1. / len(sorted_counts), len(sorted_counts)))

    ax.set_xlabel(r'number of apparances $k$')
    ax.set_ylabel(r'Cumulative, $P(t_k \geq k)$')
    ax.grid()
    fig.savefig('../figs/prepro_cumulative.pdf')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(np.arange(len(sorted_counts)) + 1, sorted_counts[::-1])
    ax.set_xlabel(r'Index $j$')
    ax.set_ylabel(r'$n_j$')
    ax.grid()
    fig.savefig('../figs/prepro_j_vs_nj.pdf')


def create_dim_reduced_data_sets():
    counter = pkl.load(open(settings.counter_fname, "r"))
    term_to_integer = dict()
    most_common = counter.most_common()
    print "Forming term to integer dict"
    for i, (term, count) in enumerate(most_common):
        term_to_integer[term] = i + 1
    print most_common[:100]
    n_diff_terms = len(most_common)

    del most_common
    del counter

    # dimension_list
    d_list = settings.d_list

    # a lot of copy paste here
    # (could be simplified)

    # frequent dim. reduction:
    if True:
        for d in d_list:
            print d
            query_fname = settings.freq_query_fnames[d]
            database_fname = settings.freq_database_fnames[d]

            with open(settings.tweets_data_fname, 'r') as f:
                # query tweets:
                with open(query_fname, "w") as f_out:
                    line_i = 0
                    while line_i < 1000:
                        line = f.readline()
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer <= d:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")
                        line_i += 1
                with open(database_fname, "w") as f_out:
                    for line in f:
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer <= d:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")

    # least frequent dim. reduction:
    if True:
        for d in d_list:
            print d
            query_fname = settings.leastfreq_query_fnames[d]
            database_fname = settings.leastfreq_database_fnames[d]

            with open(settings.tweets_data_fname, 'r') as f:
                # query tweets:
                with open(query_fname, "w") as f_out:
                    line_i = 0
                    while line_i < 1000:
                        line = f.readline()
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer >= n_diff_terms - d:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")
                        line_i += 1
                with open(database_fname, "w") as f_out:
                    for line in f:
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer >= n_diff_terms - d:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")

    # random indices
    if True:
        for d in d_list:
            print d
            valid_indices = set(np.random.choice(
                n_diff_terms, size=d, replace=False) + 1)
            query_fname = settings.random_query_fnames[d]
            database_fname = settings.random_database_fnames[d]

            with open(settings.tweets_data_fname, 'r') as f:
                # query tweets:
                with open(query_fname, "w") as f_out:
                    line_i = 0
                    while line_i < 1000:
                        line = f.readline()
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer in valid_indices:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")
                        line_i += 1
                with open(database_fname, "w") as f_out:
                    for line in f:
                        terms = line.split()
                        reduced_tweet = ""
                        for term in terms:
                            integer = term_to_integer[term]
                            if integer in valid_indices:
                                reduced_tweet = reduced_tweet + \
                                    " " + str(integer)
                        if reduced_tweet != "":
                            f_out.write(reduced_tweet[1:] + "\n")


if __name__ == "__main__":
    # to check that the tweets correspond to sets:
    # assert_tweets_are_sets()

    compute_number_of_tweets_and_plot()
    create_dim_reduced_data_sets()
