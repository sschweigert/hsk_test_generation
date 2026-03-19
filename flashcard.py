#!/usr/bin/python3

from loading import load_dataset, load_sentences, load_words
import random
import os
import argparse
from datetime import date

def parse_args():
    parser = argparse.ArgumentParser(
        description="HSK CLI tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
 
    parser.add_argument(
        "--hsk",
        type=int,
        required=True,
        choices=range(1, 7),
        metavar="{1-6}",
        help="HSK level (1–6)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="chars",
        help="Mode of operation (e.g. 'chars', 'pinyin', 'meaning')",
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        default="hard",
        help="Difficulty level ('easy' or 'hard'). Only applies to word mode.",
    )
 
    return parser.parse_args()
 
 

# Seed is based on today's date as a number
def get_seed():
    return (date.today() - date(1970, 1, 1)).days

def load_cases(hsk, mode, difficulty):
    if mode == 'words':
        words = load_words(hsk)    
        return [(key, val) for key, val in words[difficulty].items()]
    elif mode == 'chars':
        chars, data_words, pinyin = load_dataset(hsk)
        
        return [(word, val[1], val[0]) for word, val in pinyin.items()]
    else:
        raise ValueError('Unsupported mode: ' + mode)

def intro(args):
    os.system('clear')
    diff_str = 'difficulty: {}'.format(args.difficulty) if args.mode == 'words' else ''
    print('HSK: {} mode: {} {}'.format(args.hsk, args.mode, diff_str))
    input()

def show_cards(args):
    values = load_cases(args.hsk, args.mode, args.difficulty)

    random.Random(get_seed()).shuffle(values)

    for val in values:
        os.system('clear')
        for elem in val:
            print(elem)
            input()

def main():
    args = parse_args()
    intro(args)

    show_cards(args)


if __name__ == '__main__':
    main()
