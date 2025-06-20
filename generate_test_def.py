import random
import copy

non_chars = set([' ', '。', '，', '？', '！', '.', ',', '?', '!', '\"', '\'', '“', '”'])
non_chars.update([str(val) for val in range(10)])

def chars_in_sentence(sentence, chars):
    count = 0
    total = 0
    for char in sentence[0]:
        if char not in non_chars:
            total += 1
            if char in chars:
                count += 1
    return count / total

def choose_sentences(sentences, chars, count):
    chars = chars.copy()
    sentences = sentences.copy()
    to_return = []
    while len(to_return) < count:
        weights = [chars_in_sentence(sentence, chars) for sentence in sentences]
        any_nonzero = any([weight > 0 for weight in weights])
        if not any_nonzero:
            break

        result_index = random.choices(range(len(sentences)), weights=weights, k=1)[0]
        val = sentences[result_index]
        to_return.append(val)
        sentences.pop(result_index)

        for char in val[0]:
            if char in chars:
                chars.remove(char)

    k_remaining = count - len(to_return)
    if k_remaining > 0:
        additional = random.choices(sentences, k=k_remaining)
        to_return.extend(additional)
    
    random.shuffle(to_return)
    return to_return

def generate_test_def(test_config, chars, words, sentences):

    # TODO: Use local seed?
    random.seed(test_config['seed'])

    # Easy only for english->chinese
    words_english = random.sample(list(words["easy"].items()), test_config['num_words'])

    # Chinese->english contains all the remaining words (minus those in words_english)
    remaining = copy.deepcopy(words['hard']) | copy.deepcopy(words['easy'])
    for key, val in words_english:
        del remaining[key]

    words_chinese = random.sample(list(remaining.keys()), test_config['num_words'])
    
    chosen_sentences = choose_sentences(sentences, chars, test_config['num_sentences'])

    half_num = int(test_config['num_sentences'] / 2)
    
    return {
        'words_chinese':words_chinese,
        'sentences_chinese':[sentence[0] for sentence in chosen_sentences[0:half_num]],
        'words_english':[val[1] for val in words_english],
        'sentences_english':[sentence[1] for sentence in chosen_sentences[half_num:]],
        'title':'HSK {} Test'.format(str(test_config['HSK']))
    }
