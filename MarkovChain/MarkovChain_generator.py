# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 23:55:55 2017

@author: admin
"""

import MarkovChain
import pickle


if __name__ == "__main__":
    file = open(r'markov_generator', 'rb')
    markov_generator = pickle.load(file)
    out = markov_generator.generate_n_words(50)
    print(' '.join(out))