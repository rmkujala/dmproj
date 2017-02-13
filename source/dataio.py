""" Some helper functions"""


def read_tweets(fname, dtype=None):
    """
    Read tweets from a file and return them as a list of sets.

    Parameters
    ----------
    fname : str
        path to the tweeets file
    dtype : Python type, optional
        how to convert the strings into python objects
        defaulting to None (keeping them as strings)

    Returns
    -------
    tweet_list : list-like
        elements are sets of tweet terms
    """
    tweet_list = []
    with open(fname, 'r') as f:
        for line in f:
            terms = line.split()
            if dtype is not None:
                tweet_list.append(set([dtype(el) for el in terms]))
            else:
                tweet_list.append(set(terms))
    return tweet_list


def read_tweets_to_lines(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    return lines
