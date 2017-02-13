import os

""" Setting up file names and paths to various directories. """

data_dir = "/triton/becs/scratch/braindata/okoisti2/dmproj/"
if not os.path.exists(data_dir):
    data_dir = "/scratch/braindata/okoisti2/dmproj/"
assert os.path.exists(data_dir)


tweets_data_fname = data_dir + "tweets_15m.txt"
counter_fname = data_dir + "term_counter.pkl"
# quantities computed from data:
n_tweets = 14708531
n_terms = 8673357


dimreduction_types = ['freq', 'leastfreq', 'random']

# file names for various computations:
freq_query_fnames = {}
leastfreq_query_fnames = {}
random_query_fnames = {}


freq_database_fnames = {}
leastfreq_database_fnames = {}
random_database_fnames = {}

query_fnames = {}
database_fnames = {}
for dim_type, query_fname_dict, database_fname_dict in \
        zip(dimreduction_types,
            [freq_query_fnames,
             leastfreq_query_fnames,
             random_query_fnames],
            [freq_database_fnames,
             leastfreq_database_fnames,
             random_database_fnames]):
    query_fnames[dim_type] = query_fname_dict
    database_fnames[dim_type] = database_fname_dict


d_list = [100 * 2 ** (j * 2) for j in range(8)]
for d in d_list:
    random_query_fnames[d] = data_dir + \
        "query_tweets_d_random_" + str(d) + ".txt"
    freq_query_fnames[d] = data_dir + "query_tweets_d_freq_" + str(d) + ".txt"
    leastfreq_query_fnames[d] = data_dir + \
        "query_tweets_d_leastfreq_" + str(d) + ".txt"

    random_database_fnames[d] = data_dir + \
        "database_tweets_d_random_" + str(d) + ".txt"
    freq_database_fnames[d] = data_dir + \
        "database_tweets_d_freq_" + str(d) + ".txt"
    leastfreq_database_fnames[d] = data_dir + \
        "database_tweets_d_leastfreq_" + str(d) + ".txt"

eps_list = [1.5, 1.2]
# result filenames:

brute_force_fnames = {}
speedup_fnames = {}
speedup_index_fnames = {}
identity_index_fnames = {}
approx_50_fnames = {}
approx_20_fnames = {}
approx_fnames = [approx_50_fnames, approx_20_fnames]
for dimtype in dimreduction_types:
    bfdict = {}
    sudict = {}
    suidict = {}
    idict = {}
    adict_50 = {}
    adict_20 = {}
    for d in d_list:
        fname = data_dir + "brute_force_" + \
            dimtype + "_" + str(d) + ".pkl"
        bfdict[d] = fname

        fname = data_dir + "speedups_" + \
            dimtype + "_" + str(d) + ".pkl"
        sudict[d] = fname

        fname = data_dir + "speedup_index_" + \
            dimtype + "_" + str(d) + ".pkl"
        suidict[d] = fname

        fname = data_dir + "identity_index_" + \
            dimtype + "_" + str(d) + ".pkl"
        idict[d] = fname

        fname = data_dir + "approx_50_" + \
            dimtype + "_" + str(d) + ".pkl"
        adict_50[d] = fname

        fname = data_dir + "approx_20_" + \
            dimtype + "_" + str(d) + ".pkl"
        adict_20[d] = fname

    brute_force_fnames[dimtype] = bfdict
    speedup_fnames[dimtype] = sudict
    speedup_index_fnames[dimtype] = suidict
    identity_index_fnames[dimtype] = idict
    approx_50_fnames[dimtype] = adict_50
    approx_20_fnames[dimtype] = adict_20
