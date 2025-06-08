import os

# TODO: This file contains both loading as well as modification to suit latex formatting (textquotesingle...).
# Some of the formatting is OK (ie. strip), but some of the latex only stuff should be extracted so that this
# loading logic can be reused elsewhere.

# TODO: This only returns a subset of the info in the dataset. Should return more so that this can be reused elsewhere
def load_dataset(hsk):
    chars = set()
    words = {}
    filename = os.path.join('.', 'data', 'hsk' + str(hsk) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            # Note sometimes there are misc \ufeff.
            # This is due to bad CSV encoding
            split = line.replace('\ufeff', '').split('\t')
            word = split[0].strip()
            definition = split[4].strip().replace(';', ',').replace('\'','{\\textquotesingle}').capitalize()
            for char in word:
                chars.add(char)
                words[word] = definition
    return (chars, words)

def load_sentences(hsk):
    sentences = []
    filename = os.path.join('.', 'sentences', 'hsk' + str(hsk) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            split_line = line.split(';')
            if len(split_line) == 2:
                sentence = (split_line[0].strip(), split_line[1].replace('\'','{\\textquotesingle}').strip())
                sentences.append(sentence)
    return sentences

def load_words(hsk):
    words = {
        "easy": {},
        "hard": {}
    }
    filename = os.path.join('.', 'words', 'hsk' + str(hsk) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            child = 'easy' if ('*' in line) else 'hard'
            modified = line.replace('*', '').strip()
            split_line = modified.split(';')
            if len(split_line) != 2:
                continue
            word_chinese = split_line[0].strip()
            word_english = split_line[1].replace('\'','{\\textquotesingle}').strip()
            words[child][word_chinese] = word_english
    return words
