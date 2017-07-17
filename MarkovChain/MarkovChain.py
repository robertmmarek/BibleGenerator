# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:19:50 2017

@author: admin
"""

import numpy as np
import re
import pickle
import random

def markov_train(text, n_gram=2, verbose=False, special_char_as_word=False):
    tokens = tokenize(text, special_char_as_word)
    markov_t = markov_tokens(tokens, n_gram)
    markov_index = list(set(markov_t))
    markov_dict = {}
    for el, progress in zip(markov_index, range(0, len(markov_index))):
        if verbose:
            print(progress / float(len(markov_index)))
        count = float(markov_t.count(el))
        words = el.split(sep=' ')
        dict_ind = ' '.join(words[0:n_gram])
        prev_val = []
        if dict_ind in markov_dict.keys():
            prev_val = markov_dict[dict_ind]
            
        markov_dict[dict_ind] = prev_val+[(words[-1], count)]
        
    return markov_dict
    
def markov_tokens(tokens, n_gram=2):
    create_token = lambda x: ' '.join([tokens[i] for i in range(x, x+n_gram+1)])
    return [create_token(i) for i in range(0, len(tokens)-(n_gram+1))]
        

def tokenize(text, special_char_as_word=False):
    text = text.lower()
    regex_dict = {'separate': r'([A-Za-ząĄćĆęĘłŁńŃóÓśŚźŹŻż]+|[:;\.,!\?])',
                  'remove': r'([A-Za-ząĄćĆęĘłŁńŃóÓśŚźŹŻż]+)'}
    regex = regex_dict[special_char_as_word]
    tokens = [match[0] for match in re.finditer(regex, text)]
    return tokens

def load_text(path):
    text = ''
    try:
        file = open(path, 'r', encoding='utf-8')
        text = file.read()
    except Exception as e:
        print(e)
        
    return text

class MarkovGenerator:
    def __init__(self, markov_dict):
        self.n_gram = len(list(markov_dict.keys())[0].split(' '))
        self.markov_dict = markov_dict
        
    def generate_n_words(self, n=100):
        current_tokens = random.choice(list(self.markov_dict.keys())).split(' ')
        
        for i in range(0, n):
            current_key = ' '.join((current_tokens[-1:-self.n_gram-1:-1])[::-1])
            next_elements = []
            if current_key in self.markov_dict.keys():
                next_elements = self.markov_dict[current_key]
            else:
                next_elements = self.markov_dict[random.choice(list(self.markov_dict.keys()))]
            next_element = self.__random_element(next_elements)
            current_tokens += [next_element[0]]
        
        return current_tokens
    
    def __random_element(self, elements):
        el_sum = sum([el[1] for el in elements])
        select = random.uniform(0, el_sum)
        
        ret = ()
        curr_prob = 0
        for el in elements:
            curr_prob += el[1]
            if curr_prob >= select:
                ret = el
                break
            
        return ret

def main():
    text = load_text(r'bible.txt')
    markov_dict = markov_train(text, n_gram=2, verbose=True, special_char_policy='remove')
    markov_generator = MarkovGenerator(markov_dict)
    
    file = open(r'markov_generator', 'wb')
    pickle.dump(markov_generator, file)

if __name__ == "__main__":
    main()