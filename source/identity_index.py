import settings
import dataio
import cPickle as pkl

import sys

""" Create simple hash tables (tweet -> index) """


def create_identity_index(dimtype, d):
    database_fname = settings.database_fnames[dimtype][d]
    database_tweets_strs = dataio.read_tweets_to_lines(database_fname)

    # this work is done in two parts as storing lists inside of
    # the dict costs a lot of memory...

    n = len(database_tweets_strs)
    tweet_to_ind = {}
    for i, line in enumerate(database_tweets_strs):
        if i % (n / 100) == 0:
            print float(i) / n
        terms = tuple(sorted(line.split()))
        tweet_to_ind[terms] = i

    print len(tweet_to_ind)
    print i
    with open(settings.identity_index_fnames[dimtype][d], 'w') as f:
        pkl.dump(tweet_to_ind, f, pkl.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    dimtype = settings.dimreduction_types[int(sys.argv[1])]
    d = settings.d_list[int(sys.argv[2])]
    print dimtype, d

    create_identity_index(dimtype, d)
