#!/usr/bin/python3

from loading import load_dataset, load_sentences, load_words
from generate_pdf import generate_pdf
from generate_test_def import generate_test_def

# TODO: The HSK and seed can be from args
test_config = {
    'HSK': 1,
    'seed': 0,
    'num_words': 50,
    'num_sentences': 20
}


def fix_quotes(words):
    for key, val in words.items():
        words[key] = val.replace('\'','{\\textquotesingle}') 

def main():
    chars, data_words, _ = load_dataset(test_config['HSK'])
    sentences = load_sentences(test_config['HSK'])
    words = load_words(test_config['HSK'])

    fix_quotes(data_words)

    for word, definition in data_words.items():
        if word not in words["easy"]:
            words["easy"][word] = definition

    test_def = generate_test_def(test_config, chars, words, sentences)

    filename = 'output'
    generate_pdf(test_def, filename)

if __name__ == '__main__':
    main()
