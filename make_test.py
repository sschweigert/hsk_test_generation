#!/usr/bin/python3

import os
import random
import subprocess
import copy

from jinja2 import Environment, FileSystemLoader

HSK = 1

def load_dataset():
    chars = set()
    words = {}
    filename = os.path.join('.', 'data', 'hsk' + str(HSK) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            # Note sometimes there are misc \ufeff.
            # This is due to bad CSV encoding
            split = line.replace('\ufeff', '').split('\t')
            word = split[0].strip()
            definition = split[4].strip()
            for char in word:
                chars.add(char)
                words[word] = definition
    return (chars, words)

def load_sentences():
    sentences = []
    filename = os.path.join('.', 'sentences', 'hsk' + str(HSK) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            split_line = line.split(';')
            if len(split_line) == 2:
                sentence = (split_line[0].strip(), split_line[1].strip())
                sentences.append(sentence)
    return sentences

def load_words():
    words = {
        "easy": {},
        "hard": {}
    }
    filename = os.path.join('.', 'words', 'hsk' + str(HSK) + '.txt')
    with open(filename, 'r') as file:
        for line in file:
            child = 'easy' if ('*' in line) else 'hard'
            modified = line.replace('*', '').strip()
            split_line = modified.split(';')
            if len(split_line) != 2:
                continue
            word_chinese = split_line[0].strip()
            word_english = split_line[1].strip()
            words[child][word_chinese] = word_english
    return words

def choose_sentences(sentences, chars, count):
    return random.sample(sentences, count)

def main():
    chars, data_words = load_dataset()
    sentences = load_sentences()
    words = load_words()

    for word, definition in data_words.items():
        if word not in words["easy"]:
            words["easy"][word] = definition

    num_words = 50
    num_sentences = 20

    # Easy only
    easy_words = random.sample(list(words["easy"].items()), num_words)

    remaining = copy.deepcopy(words['hard']) | copy.deepcopy(words['easy'])
    for key, val in easy_words:
        del remaining[key]

    hard_words = random.sample(list(words['hard'].items()), num_words)
    
    chosen_sentences = choose_sentences(sentences, chars, num_sentences)
    half_num = int(num_sentences / 2)

    test_def = {
        'words_chinese':['中国','我们'],
        'sentences_chinese':[sentence[0] for sentence in chosen_sentences[0:half_num]],
        'words_english':[],
        'sentences_english':[sentence[1] for sentence in chosen_sentences[half_num:]]
    }
    filename = 'output.tex'
    generate_test_tex(test_def, filename)
    generate_pdf(filename)


def generate_test_tex(test_def, filename):
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('chinese_test.jinja')
    content = template.render(
        words_chinese=test_def['words_chinese'],
        sentences_chinese=test_def['sentences_chinese'],
        words_english=test_def['words_english'],
        sentences_english=test_def['sentences_english']
    )

    with open(filename, mode='w') as message:
        message.write(content)
    
def generate_pdf(tex_filename):
    subprocess.run(['xelatex', tex_filename])

if __name__ == '__main__':
    main()
