#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 

import sys
import random
import time
from text_stats import analyze_words, read_txt, output_summaries


def generate_text(starting_word, max_words_count, words_suffix_dict):
    text = starting_word
    curr_word = starting_word
    prob_cache = {}

    for _ in range(max_words_count):
        if curr_word not in words_suffix_dict:
            break
        suffix_dict = words_suffix_dict[curr_word]
        if not suffix_dict:
            break
        suffix_prob = prob_cache.get(curr_word)
        if suffix_prob is None:
            suffix_prob = list(suffix_dict.values())
            suffix_prob = [prob / sum(suffix_prob) for prob in suffix_prob]
            prob_cache[curr_word] = suffix_prob
        suffix_words = list(suffix_dict.keys())
        curr_word = random.choices(suffix_words, suffix_prob)[0]
        text += ' ' + curr_word

    return text


if __name__ == '__main__':
    args_length = len(sys.argv) if sys.argv else 0
    if (args_length <= 3):
        print('usage: test_stats.py <input_file> <starting_word> <max_words_count> [<output_file>]')
        sys.exit()

    input_filename  = sys.argv[1]
    starting_word   = sys.argv[2]
    max_words_count = int(sys.argv[3])
    output_filename = sys.argv[4] if args_length > 4 else None

    input_txt = read_txt(input_filename)
    if not input_txt:
        sys.exit()
    
    time_start = time.time()

    word_re_exp_1 = r'\w+' # hanlde one or more consecutive word characters (letters, digits, and underscores)
    word_re_exp_2 = r'\b\w+(?:\'\w+)?\b' # handle the case of 's base on word_re_exp_1
     
    _, _, words_suffix_dict = analyze_words(input_txt, re_exp=word_re_exp_2)
    somniloquy = generate_text(starting_word, max_words_count, words_suffix_dict)

    time_end = time.time()
    summary_title  = f'Generate text from file: {input_filename} with starting word: {starting_word} and max words count: {max_words_count}'
    summary_footer = f'Time cost: {time_end - time_start:.2f} seconds'

    output_summaries(output_filename, 
                     summary_title,
                     somniloquy,
                     summary_footer)
