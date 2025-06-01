#!/usr/bin/python3

import os
import random
import subprocess

from jinja2 import Environment, FileSystemLoader

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

def choose_sentences(sentences, chars, count):
    return random.sample(sentences, count)

def main():
    chars = load_chars()
    sentences = load_sentences()

    num_sentences = 10
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
