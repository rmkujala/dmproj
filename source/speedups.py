import settings
import dataio
import comps
# from get_size import total_size

from collections import Counter

import numpypy
import numpy as np

import sys
import time
import cPickle as pkl


def speedups_exact(dimtype, d):
    """
    Compute the approximate nearest neighbours for each of
    the query tweets using various speedups tricks.

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
    start_time = time.time()

    query_data_fname = settings.query_fnames[dimtype][d]
    database_fname = settings.database_fnames[dimtype][d]
    speedup_index_fname = settings.speedup_index_fnames[dimtype][d]
    identity_index_fname = settings.identity_index_fnames[dimtype][d]

    query_tweets = dataio.read_tweets(query_data_fname)

    n_querys = len(query_tweets)
    tweet_indices = np.ones(n_querys, dtype=np.int32) * -1
    angles = np.ones(n_querys, dtype=np.float32) * np.pi

    with open(identity_index_fname, mode='rb') as f:
        identity_index = pkl.load(f)

    with open(speedup_index_fname, mode="rb") as f:
        speedup_index = pkl.load(f)

    start_time = time.time()
    found = set([])
    for j, query_tweet in enumerate(query_tweets):
        tohash = tuple(sorted(query_tweet))
        if tohash in identity_index:
            angles[j] = 0
            tweet_indices[j] = int(identity_index[tohash])
            found.add(j)
    del identity_index
    database_tweets = dataio.read_tweets_to_lines(database_fname)

    print len(found), len(query_tweets)

    cur_min_tweet = -1  # index of the min distance tweet
    cur_min_angle = np.pi / 2

    for j, q_tweet in enumerate(query_tweets):
        if j in found:
            continue
        candidates = Counter()  # try first for a set

        # find candidates
        for term in q_tweet:
            if term in speedup_index:
                candidates.update(speedup_index[term])

        counts_to_candidates = []
        for candidate, count in candidates.items():
            if len(counts_to_candidates) < count:
                for i in range(count - len(counts_to_candidates)):
                    counts_to_candidates.append([])
            counts_to_candidates[count - 1].append(candidate)

        q_tweet_size = len(q_tweet)
        cur_min_tweet = -1  # index of the min distance tweet
        cur_min_angle = np.pi / 2
        for cands, count in reversed(zip(counts_to_candidates, range(1, len(counts_to_candidates) + 1))):
            distance_bound = comps.get_lower_bound(q_tweet_size, count)
            if distance_bound >= cur_min_angle:
                break
            for cand in cands:
                db_tweet = set(database_tweets[cand].split())
                angle = comps.angle(q_tweet, db_tweet)
                if angle == distance_bound:
                    cur_min_angle = angle
                    cur_min_tweet = cand
                    break

                if angle < cur_min_angle:
                    cur_min_angle = angle
                    cur_min_tweet = cand
        tweet_indices[j] = cur_min_tweet
        angles[j] = cur_min_angle
        del candidates

    # candidates.clear()

    end_time = time.time()
    return tweet_indices, angles, end_time - start_time


if __name__ == '__main__':
    dimtype = settings.dimreduction_types[int(sys.argv[1])]
    d = settings.d_list[int(sys.argv[2])]
    print dimtype, d

    tweet_indices, angles, t = speedups_exact(dimtype, d)
    # transformations due to pypy stuff:
    out_dict = {'time': t,
                'tweet_indices': [int(ind) for ind in tweet_indices],
                'angles': [float(ang) for ang in angles]}

    out_fname = settings.speedup_fnames[dimtype][d]
    with open(out_fname, "w") as f:
        pkl.dump(out_dict, f, pkl.HIGHEST_PROTOCOL)
