import os
import pickle

if __name__ == '__main__':

    # path = 'archive/'
    # output_relative_path = ''
    # index = 0
    # for filename in os.listdir(path):
    #     with open(filename, 'r', errors="ignore") as file_obj:
    #         content = file_obj.read()
    #         with open(output_relative_path + str(index) + '.txt', 'w') as f:
    #             f.write(content)
    #             index += 1
    # string = '11111.txt'
    # print(string[:-4])
    # first = {1:1,2:2 ,3:3}
    # second = {4:4,5:5}
    # first.update(second)
    # print(first)
    # dict = {'b':2,'c':3}
    # dict['a']=1
    #
    # print(dict)

    def sort_dict_by_value_asc(origin):
        after_sort = {}
        sorted_values = sorted(origin.values())
        for value in sorted_values:
            keys = find_key_based_value(origin, value)
            for key in keys:
                if key not in after_sort.keys():
                    after_sort[key] = origin[key]
        return after_sort


    def find_key_based_value(dict, target_value):
        result = []
        for key, value in dict.items():
            if value == target_value:
                result.append(key)
        return result


    def sort_dict_by_value_desc(origin):
        after_sort = {}
        sorted_values = sorted(origin.values(), reverse=True)
        for value in sorted_values:
            keys = find_key_based_value(origin, value)
            for key in keys:
                if key not in after_sort.keys():
                    after_sort[key] = origin[key]
        return after_sort

    #
    # d = {'a': 5, 'b': 4, 'c': 3, 'v': -7, 'i': 9,'l':5,'j':5}
    # a = sort_dict_by_value_asc(d)
    # print(a)
    # tuple = (1,3)
    # print(tuple[1])
    with open('doc_info.pickle', 'rb') as f_2:
        doc_info = pickle.load(f_2)

        a = doc_info[19][0]
        print(a)
