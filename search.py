import pickle
import nltk
import re
import string
from math import *
from nltk.corpus import stopwords


def find_key_based_value(dict, target_value):
    result = []
    for key, value in dict.items():
        if value == target_value:
            result.append(key)
    return result


def sort_dict_by_value_asc(origin):
    after_sort = {}
    sorted_values = sorted(origin.values())
    for value in sorted_values:
        keys = find_key_based_value(origin, value)
        for key in keys:
            if key not in after_sort.keys():
                after_sort[key] = origin[key]
    return after_sort


def sort_dict_by_value_desc(origin):
    after_sort = {}
    sorted_values = sorted(origin.values(), reverse=True)
    for value in sorted_values:
        keys = find_key_based_value(origin, value)
        for key in keys:
            if key not in after_sort.keys():
                after_sort[key] = origin[key]
    return after_sort


def calculate_score(query, doc_set):
    global doc_info
    global avg_doc_len
    global doc_num
    global index
    global k
    global b

    result = {}
    for doc_id in doc_set:
        doc_len = doc_info[doc_id][0]
        rsvd = 0

        for token in query:
            # 'sentiment':sentiment_value in the end of postings
            doc_fre = len(index[token].keys()) - 1
            in_set = list(index[token].keys())

            if doc_id in in_set:
                term_fre = index[token][doc_id]
            else:
                term_fre = 0

            value = log(doc_num / doc_fre) * ((k + 1) * term_fre) / (k * ((1 - b) + b * (doc_len / avg_doc_len)) + term_fre)
            rsvd += value

        # in index, store sum of sentiment value of all words, there need avg
        doc_sentiment_value = doc_info[doc_id][1] / doc_len
        result[doc_id] = rsvd * doc_sentiment_value
    return result


def get_sentiment_value(term):
    global index
    if term in index.keys():
        value = index[term]['sentiment']
    else:
        value = 0
    return value


def calculate_sentiment_score(query):
    score = 0
    count = 0

    for token in query:
        score += get_sentiment_value(token)
        count += 1
    content_score = score / count
    return content_score


def overlap(lst_1, lst_2):
    result = []
    index_1 = 0
    index_2 = 0

    while index_1 < len(lst_1) and index_2 < len(lst_2):
        if lst_1[index_1] == lst_2[index_2]:
            result.append(lst_1[index_1])
            index_1 = index_1 + 1
            index_2 = index_2 + 1
        elif lst_1[index_1] < lst_2[index_2]:
            index_1 = index_1 + 1
        else:
            index_2 = index_2 + 1
    return result


def union(lst_1, lst_2):
    result = lst_1[:]
    for item in lst_2:
        if item not in result:
            result.append(item)
    return result


def get_top_10(origin):
    result = []
    counter = 0
    for doc_id, score in origin.items():
        result.append(doc_id)
        counter += 1
        if counter >= 10:
            break
    return result


def search(query):
    global index

    punctuations = set(string.punctuation)
    final_search = []

    # remove all punctuation
    removed_punc = ''.join(s for s in query if s not in punctuations)

    # remove all digits
    removed_digit = re.sub(r'\d+', '', removed_punc)

    # case fold
    after_case_fold = removed_digit.lower()

    # tokenize
    doc_tokens = nltk.word_tokenize(after_case_fold)

    for token in doc_tokens:
        final_search.append(token)

    # search
    # if only one token in query
    if len(final_search) == 1:
        print(' ------ ' + query + ' ------ ')
        postings_list = list(index[final_search[0]].keys())[:-1]  # the last one is 'sentiment':sentiment_value
        ref_dict = calculate_score(final_search, postings_list)

        if calculate_sentiment_score(final_search) >= 0:   # positive
            sorted = sort_dict_by_value_desc(ref_dict)

        else:   # negative

            sorted = sort_dict_by_value_asc(ref_dict)
        top_10 = get_top_10(sorted)
        print(top_10)
        print('\n')

    else:
        filtered_tokens = [token for token in final_search if token not in stopwords.words('english')]
        query_terms_count = len(filtered_tokens)
        postings_list = list(index[filtered_tokens[0]].keys())[:-1]   # the last one is 'sentiment':sentiment_value

        print('------ ' + query + ' ------ ')

        for i in range(1, query_terms_count):
            # union hits for all tokens in query
            # the last one is 'sentiment':sentiment_value ,so [:-1]
            postings_list = union(postings_list, list(index[filtered_tokens[i]].keys())[:-1])

        ref_dict = calculate_score(filtered_tokens, postings_list)
        # sort by score value
        if calculate_sentiment_score(final_search) >= 0:  # positive
            sorted = sort_dict_by_value_desc(ref_dict)

        else:  # negative
            sorted = sort_dict_by_value_asc(ref_dict)
        # get top 10 based on sorted result
        top_10 = get_top_10(sorted)
        print(top_10)
        print('\n')


if __name__ == '__main__':

    with open('inverted_index.pickle', 'rb') as f_1:
        index = pickle.load(f_1)
    with open('doc_info.pickle', 'rb') as f_2:
        doc_info = pickle.load(f_2)

    accumulator = 0
    counter = 0
    for doc_info_r in doc_info.values():
        counter += 1
        accumulator += doc_info_r[0]

    avg_doc_len = accumulator / counter
    doc_num = counter

    k = 1.7
    b = 0.75

    search('good boy')