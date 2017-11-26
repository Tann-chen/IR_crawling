import pickle


def trans_txt_2_pickle(file_path):
    with open(file_path, 'r', errors="ignore") as f_obj:
        lines = f_obj.readlines()

    dictionary = {}

    # read line by line
    for line in lines:
        term = line.split()[0]
        value = line.split()[1]
        dictionary[term] = int(value)

    # save the dict into file
    with open('afinn.pickle', 'wb') as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)


def test():
    with open('afinn.pickle', 'rb') as f_2:
        dict = pickle.load(f_2)
        for term, value in dict.items():
            print(term + "->" + value)


if __name__ == '__main__':
    trans_txt_2_pickle('AFINN-111.txt')

