#!/usr/bin/python3

from loading import load_dataset, load_sentences, load_words
import random
import os
from datetime import date

day_as_number = (date.today() - date(1970, 1, 1)).days
print(day_as_number)

HSK = 1
seed = day_as_number

def main():
    #chars, data_words, pinyin = load_dataset(HSK)
    #
    #values = [(word, val[1], val[0]) for word, val in pinyin.items()]

    words = load_words(HSK)    
    values = [(key, val) for key, val in words['hard'].items()]

    random.Random(seed).shuffle(values)

    for val in values:
        os.system('clear')
        for elem in val:
            print(elem)
            input()
    
    

if __name__ == '__main__':
    main()
