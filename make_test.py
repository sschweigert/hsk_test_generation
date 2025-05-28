#!/usr/bin/python3

import os

HSK = 1

def load_chars():
    chars = set()
    filename = os.path.join('.', 'data', 'hsk' + str(HSK) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            word = line.split('\t')[0]
            for char in word:
                chars.add(char)
    return chars

def load_sentences():
    sentences = []
    filename = os.path.join('.', 'sentences', 'hsk' + str(HSK) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            split_line = line.split(';')
            if len(split_line) == 2:
                sentence = (split_line[0], split_line[1])
                sentences.append(sentence)
    return sentences

def main():
    chars = load_chars()
    sentences = load_sentences()
    
    

if __name__ == '__main__':
    main()
