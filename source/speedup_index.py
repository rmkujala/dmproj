import settings
import dataio
import sys
import cPickle as pkl


def create_speedup_index(dimtype, d):
    database_fname = settings.database_fnames[dimtype][d]
    database_tweets_strs = dataio.read_tweets_to_lines(database_fname)

    n = len(database_tweets_strs)
    term_to_tweets = {}
    for i, line in enumerate(database_tweets_strs):
        if i % (n / 100) == 0:
            print float(i) / n
        terms = line.split()
        for term in terms:
            if term in term_to_tweets:
                term_to_tweets[term].append(i)
            else:
                term_to_tweets[term] = [i]

    n_terms = len(term_to_tweets)
    print n_terms

    with open(settings.speedup_index_fnames[dimtype][d], 'w') as f:
        pkl.dump(term_to_tweets, f, pkl.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    dimtype = settings.dimreduction_types[int(sys.argv[1])]
    d = settings.d_list[int(sys.argv[2])]
    print dimtype, d
