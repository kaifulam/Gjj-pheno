__author__ = 'julian, modified by Dennis'

import numpy as np
import fileinput
import re
from ast import literal_eval
import random


def parse_line(line, add_padding=True):
    # parses a line to make it numpy friendly and returns it with tuple format as a string (for concatenation)
    #track_size, vertex_size, max_tracks = 8, 5, 15
    track_size, covariance_size, weight_size, vertex_size, max_tracks = 5, 15, 1, 7, 15
    num_per_track = track_size + covariance_size + weight_size + vertex_size
    num_high_level = 14 + 2
    num_mid_level = max_tracks * num_per_track + 2

    line = replace_non_num_with_nan(line)
    line = replace_bracket_with_parenthesis(line)

    general_high_level_and_y, mid_level = separate_features(line)

    mid_level = replace_parenthesis_with_sqr_bracket(mid_level)
    general_high_level_and_y = replace_parenthesis_with_sqr_bracket(general_high_level_and_y)
    general, y, general_and_high_level = separate_general_high_level_and_y(general_high_level_and_y)

    general_and_high_level = flatten_tuple(general_and_high_level)
    assert len(literal_eval('(%s)' % general_and_high_level)) == num_high_level

    if len(mid_level) == 0 or len(mid_level) == 1:
        return [False, False, False]  # tracks are empty, discard sample

    mid_level, num_tracks_in_sample = sort_and_prune_tracks(mid_level, max_tracks)
    if add_padding:
        padding = ", 'nan'" * (num_per_track * (max_tracks - num_tracks_in_sample))
        mid_level = mid_level + padding

    mid_level = flatten_tuple(mid_level)
    general_and_mid_level = add_general_to_mid(general, mid_level)
    assert_size_mid_level(general_and_mid_level, num_mid_level)

    return [y, general_and_high_level, general_and_mid_level]


def add_general_to_mid(general, mid_level):
    general_and_mid_level = '[' + general + ', ' + mid_level[1:]
    return general_and_mid_level


def assert_size_mid_level(mid_level, num_mid_level):
    if not len(literal_eval('(%s)' % mid_level)) == num_mid_level:
        print(mid_level)
        print('len(literal_eval((%s) % mid_level))', len(literal_eval('(%s)' % mid_level)))
        print('num_mid_level', num_mid_level)
        return [False, False, False]


def separate_features(line):
    general_high_level_and_y = line.split("[")[0]
    general_high_level_and_y = re.sub(r"[[]", "", general_high_level_and_y)

    mid_level = line.split("[")[1]
    mid_level = re.sub(r"[]]", "", mid_level)

    return [general_high_level_and_y, mid_level]


def sort_and_prune_tracks(mid_level, max_tracks):
    # sort and prune are together so the input and output are both string versions of the array
    if "]]," not in mid_level:  # only has one track
        return [mid_level, 1]

    mid_level = replace_parenthesis_with_sqr_bracket(mid_level)

    track_array = string_to_array(mid_level)

    #track_array = sorted(track_array, reverse=True, key=get_d0)  # sort by highest d0 first (first number on each track)
    #track_array = sorted(track_array, reverse=True, key=get_d0)
    track_array = sorted(track_array, reverse=True, key=get_d0_significance)

    if len(track_array) > max_tracks:
        track_array = track_array[0:max_tracks]

    mid_level = array_to_string(track_array)

    return [mid_level, len(track_array)]


def get_d0(track):
    return abs(track[0][0])


def get_d0_significance(track):
    d0 = track[0][0]
    d0_uncertainty = track[1][0]
    if d0 == 'nan' or d0_uncertainty == 'nan' or d0_uncertainty == 0:
        return -1  # will be less than any other value due to absolute value
    return abs(d0 / (1.0 * d0_uncertainty))


def separate_general_high_level_and_y(high):
    high_array = string_to_array(high)
    general = array_to_string(high_array[0:2])
    y = str(high_array.pop(2))
    high = array_to_string(high_array)
    return [general, y, high]


def string_to_array(list_of_elements):
    list_of_elements = '[' + list_of_elements + ']'
    return literal_eval('(%s)' % list_of_elements)


def array_to_string(arr):
    array_as_string = str(arr)
    return array_as_string[1:len(array_as_string) - 1]


def replace_non_num_with_nan(l):
    l = re.sub('-inf', "None", l)
    l = re.sub('inf', "None", l)
    l = re.sub('-nan', "None", l)
    l = re.sub('nan', "None", l)
    l = re.sub('None', "'nan'", l)
    return l


def replace_bracket_with_parenthesis(l):
    l = re.sub(r"[{]", "(", l)
    l = re.sub(r"[}]", ")", l)
    return l


def replace_parenthesis_with_sqr_bracket(l):
    l = re.sub(r"[(]", "[", l)
    l = re.sub(r"[)]", "]", l)
    return l


def flatten_tuple(text):
    text = re.sub(r'[\[]', "", text)
    text = re.sub(r'[]]', "", text)
    text = '[' + text + ']'
    return text


def print_head(open_file, n_lines=10):
    i = 0
    while i < n_lines:
        line = open_file.readline()
        if len(line) > 2:
            print(parse_line(line))
            i += 1


def count_tracks(open_file):
    histogram = np.zeros(100, dtype='i')
    min_tracks = 100000
    max_tracks = 0
    total_tracks = 0
    total_lines = 0
    bad_lines = 0
    for line in open_file.readlines():
        if len(line) > 2:
            total_lines += 1
            num_tracks = count_tracks_per_sample(line)
            total_tracks += num_tracks
            if num_tracks > max_tracks:
                max_tracks = num_tracks
            if num_tracks < min_tracks:
                min_tracks = num_tracks
            if num_tracks == 0:
                bad_lines += 1
            histogram[num_tracks] += 1
    average = total_tracks / total_lines

    print('number of samples', total_lines)
    print('average', average)
    print('min_tracks', min_tracks)
    print('max_tracks', max_tracks)
    print('bad lines', bad_lines)
    print('histogram', histogram)
    return histogram

def count_tracks_per_sample(line):
    track_size, covariance_size, weight_size, vertex_size, max_tracks = 5, 15, 1, 7, 15
    num_per_track = track_size + covariance_size + weight_size + vertex_size
    num_high_level = 14 + 2
    num_mid_level = max_tracks * num_per_track + 2

    line = replace_non_num_with_nan(line)
    line = replace_bracket_with_parenthesis(line)

    general_high_level_and_y, mid_level = separate_features(line)

    mid_level = replace_parenthesis_with_sqr_bracket(mid_level)

    if len(mid_level) == 0 or len(mid_level) == 1:
        return 0  # tracks are empty, discard sample

    num_tracks_in_sample = get_num_tracks_from_mid_level(mid_level)

    return num_tracks_in_sample


def get_num_tracks_from_mid_level(mid_level):
    if "]]," not in mid_level:  # only has one track
        return 1

    mid_level = replace_parenthesis_with_sqr_bracket(mid_level)

    track_array = string_to_array(mid_level)

    return len(track_array)


def clean_and_merge_lines(open_file, batchsize, filename, save_path):
    # Cleans the whole dataset and returns it as a list of arrays with the strings of each batch of size batchsize
    # separated by label, high and mid level features
    # ### WARNING ### it discards the last batch samples if incomplete
    # This solves memory problems as long as the whole string is loadable to memory and one of the batches in numpy form

    data_string_y = "["
    data_string_high = "["
    data_string_mid = "["
    total_in_this_batch = 0
    batch = 0

    for line in open_file.readlines():
        if len(line) > 2:
            y, high_level, mid_level = parse_line(line)  # a good line has both high and mid-level features [high_level, mid_level]
            if y and high_level and mid_level:
                data_string_y = data_string_y + y + ', '
                data_string_high = data_string_high + high_level + ', '
                data_string_mid = data_string_mid + mid_level + ', '
                total_in_this_batch += 1
                if total_in_this_batch == batchsize:
                    data_string_y = data_string_y + "]"
                    data_string_high = data_string_high + ']'
                    data_string_mid = data_string_mid + ']'

                    batch_number = "_" + str(batch)

                    save_batch_as_np_array(data_string_y, filename, save_path, "y", batch_number=batch_number)
                    save_batch_as_np_array(data_string_high, filename, save_path, "high", batch_number=batch_number)
                    save_batch_as_np_array(data_string_mid, filename, save_path, "mid", batch_number=batch_number)

                    data_string_y, data_string_high, data_string_mid = "[", "[", "["
                    total_in_this_batch = 0
                    batch += 1
    return


def save_batch_as_np_array(text, filename, save_path, feature_type, batch_number=""):
    data = np.asarray(literal_eval('(%s)' % text), dtype='f')
    print("saving batch" + batch_number, feature_type)
    if feature_type == 'high':
        assert data.shape[1] == 14 + 2
    if feature_type == 'mid':
        assert data.shape[1] == 420 + 2

    if 'signal' in filename:
        np.save(save_path + 'clean_signal-dijet' + "_" + feature_type + batch_number, data)
    elif 'bg' in filename:
        np.save(save_path + 'clean_bg-dijet' + "_" + feature_type + batch_number, data)
    else:
        assert 1==0  # Files were not generated. There is a problem with the source filename




#load_path = './'
load_path = "/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/"

#filename = "dijet-bg.txt.gz"
#filename = "all-signal.json"
#filename = 'ten_line_signal.json'
filename = 'one_line_signal.json'

filename = load_path + filename


#save_path = './saved_batches/'
save_path = "/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/high_mid_low_and_covariance/numpy_data/batches_5000/"


if filename[-3:] == '.gz':  # Check if the file is compressed or not and open accordingly
    fid = fileinput.hook_compressed(filename, 'r')
else:
    fid = open(filename)

clean_and_merge_lines(fid, 1, filename, save_path)
