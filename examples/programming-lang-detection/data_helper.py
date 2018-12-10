#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import codecs
import defs
import re
import numpy as np
import requests

train_root_folder = 'data/train'
test_root_folder = 'data/test'
snippets_per_file = 3


def get_input_and_labels(root_folder=train_root_folder, file_vector_size=10 * 1024, max_files=1000, breakup=False):
    """
    :return: char_inputs, class_vec, file_names
    char_inputs is a an array of inputs where each input is a padded array of quantised character one-hot vectors
    class_vec is basically one-hot vector of the class definition
    file_names is array of file names. It can contain duplicates if file has been split
    """

    class_vec = []
    langs = defs.langs
    n_classes = len(langs)
    print(n_classes)
    char_inputs = []
    file_names = []
    i = 0


    for fld in langs:
        vect = [0 for x in range(0, n_classes)]
        vect[i] = 1
        print(fld)
        folder = os.path.join(root_folder, fld)
        n = 0
        for file in os.listdir(folder):
            if n > max_files:
                break
            file_name = os.path.join(folder, file)
            try:
                file_vectors = turn_file_to_vectors(file_name,
                                                    file_vector_size, breakup=breakup)
                for fv in file_vectors:
                    char_inputs.append(fv)
                    class_vec.append(vect)
                    file_names.append(file_name)
                n += 1
            except:
                print(e)
        i += 1

    return np.array(char_inputs), np.array(class_vec), file_names


def get_text_and_labels(root_folder=train_root_folder, max_files=1000,
                        breakup=False):
    """
    :return: text_arr, class_def
    text_arr is a an array of text
    class_def is basically one-hot vector of the class definition
    """

    class_def = []
    langs = defs.langs
    n_classes = len(langs)
    print(n_classes)
    text_arr = []
    i = 0
    for fld in langs:
        vect = [0 for x in range(0, n_classes)]
        vect[i] = 1
        print(fld)
        folder = os.path.join(root_folder, fld)
        n = 0
        for file in os.listdir(folder):
            if n > max_files:
                break
            file_name = os.path.join(folder, file)
            try:
                snippets = get_text_or_snippets(file_name, breakup)
                for txt in snippets:
                    text_arr.append(txt)
                    class_def.append(vect)
                n += 1
            except:
                print(e)
        i += 1

    return (np.array(text_arr), np.array(class_def))


def turn_url_to_vector(f_url, file_vector_size=10 * 1024,
                       normalise_whitespace=True):
    response = requests.get(f_url)
    return turn_text_to_vector(response.text, file_vector_size,
                               normalise_whitespace)


def turn_text_to_vector(text, file_vector_size=10 * 1024,
                        normalise_whitespace=True):
    """
    extracts feature vector from text
    :param text: text
    :param file_vector_size: size of the vector
    :param normalise_whitespace: replacing all whitespace to space
    :return: vector
    """

    file_vector = []  # will be byte array

    # Normalising whitespace
    # NOTE: this could backfire due to whitespace significant languages
    # but allows for more code consumed

    if normalise_whitespace:
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t',
                                                                  ' ')
        text = re.sub('\s+', ' ', text)

    text = text[0:file_vector_size]
    for char in text:
        if char in defs.supported_chars_map:
            file_vector.append(defs.supported_chars_map[char])

    if len(file_vector) < file_vector_size:
        for j in range(0, file_vector_size - len(file_vector)):
            file_vector.append(defs.pad_vector)

    return np.array(file_vector)


def get_text_or_snippets(file_name, breakup=False):
    """
    either returns array of texts
    :param file_name: name of the file
    :return: text or list of snippets
    """

    text = ''
    with codecs.open(file_name, mode='r', encoding='utf-8') as f:
        text = f.read().lower()
    lines = text.split('\n')
    nlines = len(lines)
    if breakup and nlines > 50:
        third = nlines / snippets_per_file
        twoThird = 2 * third
        text2 = '\n'.join(lines[third:twoThird])
        text3 = '\n'.join(lines[twoThird:])
        return [text, text2, text3]
    else:
        return [text]


def turn_file_to_vectors(
        file_name,
        file_vector_size=10 * 1024,
        normalise_whitespace=True,
        breakup=False,
):
    texts = get_text_or_snippets(file_name, breakup)
    return [turn_text_to_vector(t, file_vector_size,
                                normalise_whitespace) for t in texts]



