import sys
import re
import os
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet


def cast_dict_2_str(dict):
    result = ''
    for key, value in dict.items():
        result = result + key + ':{' + cast_dict_2_str_2(value) + '}\n'
    return result


def cast_dict_2_str_2(dict):
    result = ''
    for key, value in dict.items():
        result = result + str(key) + ':' + str(value) + ','
    return result


def sort_dict(origin):
    after_sort = {}
    sorted_keys = sorted(origin.keys())
    for key in sorted_keys:
        after_sort[key] = origin[key]
    return after_sort


def sort_posting_list(index):
    after_sort = {}
    for term, posting_lst in index.items():
        after_sort[term] = sort_dict(posting_lst)
    return after_sort


def get_sentiment_value(term):
    global sentiment_dict
    if term in sentiment_dict:
        score = sentiment_dict[term]
    else:
        score = 0
    return score


def add_sentiment_to_index(final_index):
    for term, postings in final_index.items():
        # postings is a dict
        postings['sentiment'] = get_sentiment_value(term)


def spimi(input_folder):
    global memory_size
    global block_size
    global relative_path

    punctuations = set(string.punctuation)
    output_file_index = 0
    postings = {}
    doc_info_dict = {}

    for filename in os.listdir(input_folder):
        with open(input_folder + filename, 'r', errors="ignore") as file_obj:
            doc_content = file_obj.read()
            doc_id = int(filename[:-4])

        print(input_folder + filename + ' is being processed (doc_id:' + str(doc_id) + ')')


        # remove all punctuation
        removed_punc = ''.join(s for s in doc_content if s not in punctuations)

        # remove all digits
        removed_digit = re.sub(r'\d+', '', removed_punc)

        # case fold
        after_case_fold = removed_digit.lower()

        # tokenize
        doc_tokens = nltk.word_tokenize(after_case_fold)

        # record the doc length
        doc_length = len(doc_tokens)

        # sentiment accumulator
        sentiment_accumulator = 0

        # filter all no-english words
        filtered_no_english_tokens = [token for token in doc_tokens if wordnet.synsets(token)]

        # filter stop words
        filtered_tokens = [token for token in filtered_no_english_tokens if token not in stopwords.words('english')]

        # add into posting
        for token in filtered_tokens:

            # counting sentiment
            sentiment_accumulator += get_sentiment_value(token)

            # add token into index
            if token in postings.keys():
                postings_list = postings[token]  # postings_list is {doc_id:tf, doc_id:tf, doc_id:tf}
                in_docs = postings_list.keys()  # find all doc_id in the posting list

                if doc_id in in_docs:  # if the doc_id is already in the posting list
                    postings_list[doc_id] += 1  # tf += 1
                else:
                    postings_list[doc_id] = 1  # add the doc_id into posting list and tf = 1
            else:  # a now term in index
                new_postings_list = {doc_id: 1}
                postings[token] = new_postings_list

        # one doc done
        doc_info_dict[doc_id] = (doc_length, sentiment_accumulator)

        # check block size
        if sys.getsizeof(postings) >= memory_size * 1024 * 1024:
            # write into disk
            with open(relative_path + str(output_file_index) + '.pickle', 'wb') as f:
                pickle.dump(sort_dict(postings), f, pickle.HIGHEST_PROTOCOL)
            with open(relative_path + str(output_file_index) + '.txt', 'w') as f:
                f.write(cast_dict_2_str(sort_dict(postings)))

            output_file_index += 1
            # new postings
            postings.clear()

    # write the final postings into block
    with open(relative_path + str(output_file_index) + '.txt', 'w') as f:
        f.write(cast_dict_2_str(sort_dict(postings)))
    with open(relative_path + str(output_file_index) + '.pickle', 'wb') as f:
        pickle.dump(sort_dict(postings), f, pickle.HIGHEST_PROTOCOL)

    with open('doc_info.pickle', 'wb') as f_2:
        pickle.dump(doc_info_dict, f_2, pickle.HIGHEST_PROTOCOL)

    print('====== SPIMI done ======')
    return output_file_index


def blocks_merge(blocks_count):
    global relative_path

    if blocks_count > 0:
        block_index = 0

        # load first postings_lists
        with open(relative_path + str(block_index) + '.pickle', 'rb') as f:
            pl_first = pickle.load(f)
            block_index = block_index + 1

        if blocks_count == 1:
            # sort every posting list based on doc_id
            final = sort_posting_list(pl_first)

            # add sentiment value for every token
            add_sentiment_to_index(final)

            with open('inverted_index.pickle', 'wb') as f:
                pickle.dump(final, f, pickle.HIGHEST_PROTOCOL)
            with open('inverted_index.txt', 'w') as f:
                f.write(cast_dict_2_str(final))

        else:  # multiple blocks
            while block_index < blocks_count:
                with open(relative_path + str(block_index) + '.pickle', 'rb') as f:
                    pl_second = pickle.load(f)
                    print(str(block_index) + '.pickle is being merging with master')

                # merge two blocks
                pl_first_terms = list(pl_first.keys())
                pl_first_len = len(pl_first_terms)
                pl_1 = 0

                pl_second_terms = list(pl_second.keys())
                pl_second_len = len(pl_second_terms)
                pl_2 = 0

                while pl_1 < pl_first_len and pl_2 < pl_second_len:
                    if pl_first_terms[pl_1] == pl_second_terms[pl_2]:
                        temp_dict = pl_second[pl_second_terms[pl_2]]
                        # merge pl_second's posting list to pl_first - add {} to {}
                        pl_first[pl_first_terms[pl_1]].update(temp_dict)

                        # sort
                        pl_first[pl_first_terms[pl_1]] = sort_dict(pl_first[pl_first_terms[pl_1]])
                        pl_1 = pl_1 + 1
                        pl_2 = pl_2 + 1

                    elif pl_first_terms[pl_1] < pl_second_terms[pl_2]:
                        pl_1 = pl_1 + 1

                    else:
                        temp_term = pl_second_terms[pl_2]
                        temp_dict = pl_second[temp_term]
                        pl_first[temp_term] = sort_dict(temp_dict)
                        pl_2 = pl_2 + 1

                if pl_1 < pl_first_len:  # pl_2 have done, not new for pl_1
                    pass

                if pl_2 < pl_second_len:
                    while pl_2 < pl_second_len:
                        temp_term = pl_second_terms[pl_2]
                        temp_dict = pl_second[temp_term]
                        pl_first[temp_term] = sort_dict(temp_dict)
                        pl_2 = pl_2 + 1

                # after merge two blocks
                # pl_first = sort_dict(pl_first)
                block_index = block_index + 1

            # finish all merging
            # add sentiment value for every token
            add_sentiment_to_index(pl_first)
            with open('inverted_index.pickle', 'wb') as f:
                pickle.dump(pl_first, f, pickle.HIGHEST_PROTOCOL)
            with open('xx_inverted_index.txt', 'w') as f:
                f.write(cast_dict_2_str(pl_first))

    print('====== Merge done ======')


if __name__ == '__main__':
    with open('afinn.pickle', 'rb') as f:
        sentiment_dict = pickle.load(f)

    relative_path = 'postings/'
    memory_size = 1  # MB
    block_size = 1  # MB
    input_folder = 'repo/'

    # spimi(input_folder)
    blocks_merge(1)
    print("====== Done ======")
