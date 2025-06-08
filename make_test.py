#!/usr/bin/python3

import os
import random
import subprocess
import copy

from jinja2 import Environment, FileSystemLoader

HSK = 1
random.seed(0)

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
            definition = split[4].strip().replace(';', ',').replace('\'','{\\textquotesingle}').capitalize()
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
                sentence = (split_line[0].strip(), split_line[1].replace('\'','{\\textquotesingle}').strip())
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
            word_english = split_line[1].replace('\'','{\\textquotesingle}').strip()
            words[child][word_chinese] = word_english
    return words

def chars_in_sentence(sentence, chars):
    count = 0
    total = 0
    for char in sentence[0]:
        if char != ' '
            total += 1
            if char not in chars
                count += 1
    return count
        

def choose_sentences(sentences, chars, count):
    chars = chars.copy()
    sentences = sentences.copy()
    to_return = []
    while len(to_return) < count:
        weights = [chars_in_sentence(sentence) for sentence in sentences]
        any_nonzero = any([weight > 0 for weight in weights])
        if not any_nonzero:
            break

        result_index = random.choices(range(len(sentences)), weights=weights, k=1)
        val = sentences[result_index]
        to_return.append(val)
        sentences.pop(result_index)

        for char in val:
            chars.remove(char)

    k_remaining = count - len(to_return)
    if k_remaining > 0:
        additional = random.choices(sentences, k=k_remaining)
        to_return.extend(additional)
    
    random.shuffle(to_return)
    return to_return

def main():
    chars, data_words = load_dataset()
    sentences = load_sentences()
    words = load_words()

    for word, definition in data_words.items():
        if word not in words["easy"]:
            words["easy"][word] = definition

    num_words = 50
    num_sentences = 20

    # Easy only for english->chinese
    words_english = random.sample(list(words["easy"].items()), num_words)

    # Chinese->english contains all the remaining words (minus those in words_english)
    remaining = copy.deepcopy(words['hard']) | copy.deepcopy(words['easy'])
    for key, val in words_english:
        del remaining[key]

    words_chinese = random.sample(list(remaining.keys()), num_words)
    
    chosen_sentences = choose_sentences(sentences, chars, num_sentences)
    half_num = int(num_sentences / 2)

    test_def = {
        'words_chinese':words_chinese,
        'sentences_chinese':[sentence[0] for sentence in chosen_sentences[0:half_num]],
        'words_english':[val[1] for val in words_english],
        'sentences_english':[sentence[1] for sentence in chosen_sentences[half_num:]],
        'title':'HSK {} Test'.format(str(HSK))
    }
    filename = 'output.tex'
    generate_test_tex(test_def, filename)
    generate_pdf(filename)


def generate_test_tex(test_def, filename):
    env = Environment(loader=FileSystemLoader('templates/'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('chinese_test.jinja')
    content = template.render(
        words_chinese=test_def['words_chinese'],
        sentences_chinese=test_def['sentences_chinese'],
        words_english=test_def['words_english'],
        sentences_english=test_def['sentences_english'],
        title=test_def['title']
    )

    with open(filename, mode='w') as message:
        message.write(content)
    
def generate_pdf(tex_filename):
    subprocess.run(['xelatex', tex_filename])

if __name__ == '__main__':
    main()
