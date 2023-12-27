#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 

import re
import sys
import time
import numpy as np


def analyze_letters(txt, sort=True):
    letter_array = np.array(re.findall('[a-zA-Z]', txt))
    letters, counts = np.unique(letter_array, return_counts=True)
    if sort:
        sorted_indices  = np.argsort(-counts)
        letters = letters[sorted_indices]
        counts  = counts[sorted_indices]

    return (tuple(letters), tuple(counts))

def summay_letter_stats(freq_stats):
    letters, counts = freq_stats
    summary = "{:<6} {:<8}".format('Letter','Count')
    for i in range(len(letters)):
        summary += "\n" + "{:<6} {:<8}".format(letters[i], counts[i])

    return summary

def analyze_words(txt, re_exp = r'[a-zA-Z]+', sort=True):
    words_list = re.findall(re_exp, txt)
    words_array = np.array(words_list)
    
    # frequency statistics
    total_words_count = words_array.shape[0]
    words, counts  = np.unique(words_array, return_counts=True)
    if sort:
        sorted_indices  = np.argsort(-counts)
        words  = words[sorted_indices]
        counts = counts[sorted_indices]
    freq_stats = (tuple(words), tuple(counts))

    # words chain
    tmp_dict = {}
    for i in range(1, len(words_list)):
        curr = words_list[i]
        prev = words_list[i-1]
        if prev not in tmp_dict:
            tmp_dict[prev] = {}
        if curr not in tmp_dict[prev]:
            tmp_dict[prev][curr] = 0
        tmp_dict[prev][curr] += 1

    suffix_dict = {}
    if sort:
        for word, suffix in tmp_dict.items():
            sorted_suffix = dict(sorted(suffix.items(), key=lambda item: item[1], reverse=True))
            suffix_dict[word] = sorted_suffix
    else:
        suffix_dict = tmp_dict
    
    return total_words_count, freq_stats, suffix_dict

def summary_words_stats(freq_stats, suffix_dict):
    top5 = freq_stats[0][:5]
    top5_freq = freq_stats[1][:5]

    top3_suffix = [list(suffix_dict[key].keys())[:3] for key in top5]
    top3_suffix_freq = [list(suffix_dict[key].values())[:3] for key in top5]

    summary = "5 most commonly used words and 3 words that most commonly follow them." + "\n"
    for i in range(len(top5)):
        summary += f"{top5[i]} ({top5_freq[i]} occurrences)" + "\n"

        curr_suffix = top3_suffix[i]
        curr_suffix_freq = top3_suffix_freq[i]
        for j in range(len(curr_suffix)):
            summary += f"-- {curr_suffix[j]}, {curr_suffix_freq[j]}" + "\n"

    return summary

def output_summaries(output_filename, *summaries):
    summary = ""
    for s in summaries:
        summary += s + "\n\n"
    
    if output_filename is None:
        print(summary)
    else:
        with open(output_filename, 'w') as output_file:
            output_file.write(summary)

def read_txt(input_filename, lower_case = True):
    try:
        with open(input_filename, 'r') as input_file:
            input_txt = input_file.read()
        if not input_txt:   
            print(f'The file is empty: {input_filename}')
        return input_txt if not lower_case else input_txt.lower()
    except FileNotFoundError:
        print(f'The file does not exist: {input_filename}')


if __name__ == '__main__':
    args_length = len(sys.argv) if sys.argv else 0
    if (args_length <= 1):
        print('usage: test_stats.py <input_file> [<output_file>]')
        sys.exit()

    input_filename  = sys.argv[1]
    output_filename = sys.argv[2] if args_length > 2 else None

    input_txt = read_txt(input_filename)
    if not input_txt:
        sys.exit()
    
    time_start = time.time()

    # letters statistics
    letters_freq_stats = analyze_letters(input_txt)
    letters_summary = summay_letter_stats(letters_freq_stats)
    # words statistics
    total_words_count, words_freq_stats, words_suffix_dict = analyze_words(input_txt)
    words_count_summary = f'Total number of words: {total_words_count} and unique words: {len(words_freq_stats[0])}'
    words_detail_summary = summary_words_stats(words_freq_stats, words_suffix_dict)

    time_end = time.time()
    summary_title = f'Summary about file: {input_filename}'
    summary_footer = f'Time cost: {(time_end - time_start):.3f} seconds'
    
    output_summaries(output_filename, 
                     summary_title, 
                     letters_summary,
                     words_count_summary,
                     words_detail_summary, 
                     summary_footer)