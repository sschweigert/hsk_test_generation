#!/usr/bin/python3

from loading import load_dataset, load_sentences, load_words
import random
import os

HSK = 1
seed = 1

def main():
    chars, data_words, pinyin = load_dataset(HSK)
    
    values = [(word, val[1], val[0]) for word, val in pinyin.items()]

    random.Random(seed).shuffle(values)

    for val in values:
        os.system('clear')
        print(val[0])
        input()
        print(val[1])
        input()
        print(val[2])
        input()
    
    

if __name__ == '__main__':
    main()
