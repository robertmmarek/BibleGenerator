# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 23:55:55 2017

@author: admin
"""

import MarkovChain
import pickle

from matplotlib import pyplot as pp


if __name__ == "__main__":
    file = open(r'markov_generator', 'rb')
    markov_generator = pickle.load(file)
    counts = markov_generator.calc_stats()
    
    print(counts[1]/sum(counts[counts.index[:]]))

    out = markov_generator.generate_n_words(1000)
    print(' '.join(out))