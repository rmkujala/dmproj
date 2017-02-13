import settings
import dataio
import comps

import numpypy
import numpy as np

import sys
import time

import pickle as pkl


def brute_force(dimtype, d):
    """
    Compute the nearest neighbours for each of the query tweets
    by looping over the 1000 query tweets and the database tweets.

    Parameters
    ----------
    dimtype : str
            either 'freq', 'leastfreq' or 'random'
    d : int
            one of the elements in the settings.d_list

    Returns
    -------
    tweet_indices : np.array of size 1000, dtype=int
            the indices of the tweets
            (index 0 means the first line in the tweets database)
    angles : np.array of size 1000, dtype=float
            the corresponding smallest angles to tweets
    time : float
            time spent for execution in seconds
    """
    query_data_fname = settings.query_fnames[dimtype][d]
    database_fname = settings.database_fnames[dimtype][d]
    query_tweets = dataio.read_tweets(query_data_fname)

    n_querys = len(query_tweets)
    tweet_indices = np.ones(n_querys, dtype=np.int32) * -1
    angles = np.ones(n_querys, dtype=np.float32) * np.pi

    start_time = time.time()
    with open(database_fname, 'r') as db_file:
        # loop over databse lines (tweets):
        for i, line in enumerate(db_file):
            database_tweet = set(line.split())
            for j, query_tweet in enumerate(query_tweets):
                new_angle = comps.angle(database_tweet, query_tweet)
                if new_angle < angles[j]:
                    angles[j] = new_angle
                    tweet_indices[j] = i

    end_time = time.time()
    return tweet_indices, angles, end_time - start_time


if __name__ == '__main__':
    dimtype = settings.dimreduction_types[int(sys.argv[1])]
    d = settings.d_list[int(sys.argv[2])]
    print dimtype, d

    tweet_indices, angles, t = brute_force(dimtype, d)
    # transformations due to pypy stuff:
    out_dict = {'time': t,
                'tweet_indices': [int(ind) for ind in tweet_indices],
                'angles': [float(ang) for ang in angles]}

    out_fname = settings.brute_force_fnames[dimtype][d]
    with open(out_fname, "w") as f:
        pkl.dump(out_dict, f)
