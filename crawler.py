from bs4 import BeautifulSoup
import requests
import re
import pickle
import afinnreader

threshold = 2

def save_list(filepath, list):
    with open(filepath, 'wb') as f:
        pickle.dump(list, f, pickle.HIGHEST_PROTOCOL)


def read_list(filepath):
    list = pickle.load(open(filepath, "rb"))
    return list


def recursive_get_link(links, i):
    global rootdir
    global file
    file = 'output2.pickle'

    save_list(file, links)
    if i > threshold:
        return
    page_links = []
    for link in links:
        new_page_links = get_links_within_page(link)
        page_links += new_page_links
    x = recursive_get_link(page_links, i + 1)
    page_links += x
    return page_links


def get_links_within_page(url):
    current_page_links = []
    try:
        response = requests.get(url, timeout=2)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        a_tags = soup.findAll('a')

        for a in a_tags:
            if 'href' in a.attrs.keys():
                link = a['href']
                if 'mailto' not in link:
                    if link[:4] == 'http' or link[:3] == 'www':
                        x = link
                        # links_container.append(link)
                    else:
                        x = url + link
                        # current_page_links.append(url + link)
                        # links_container.append(url + link)  # relative path
                y = x.split(" ")
                current_page_links.append(y[0])

    except requests.exceptions.RequestException as e:
        print('*** one exception in request for crawling page ***')
        print(str(e))

    return current_page_links


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)


def stripcomment(data):
    p = re.compile('(<!--.*?-->)', flags=re.DOTALL)
    return p.sub(' ', data)


def stripurl(data):
    p = re.compile(r"http\S+", flags=re.DOTALL)
    return p.sub(' ', data)


def extract_text(target_url):
    global index
    global relative_path

    try:
        response = requests.get(target_url, timeout=2)
        soup = BeautifulSoup(response.text, 'html.parser')

        page_content = ''

        if len(soup.findAll('body')) > 0:
            h1_tags = soup.body.findAll('h1')
            for h1 in h1_tags:
                page_content = page_content + ' ' + h1.text

            h2_tags = soup.body.findAll('h2')
            for h2 in h2_tags:
                page_content = page_content + ' ' + h2.text

            h3_tags = soup.body.findAll('h3')
            for h3 in h3_tags:
                page_content = page_content + ' ' + h3.text

            h4_tags = soup.body.findAll('h4')
            for h4 in h4_tags:
                page_content = page_content + ' ' + h4.text

            h5_tags = soup.body.findAll('h5')
            for h5 in h5_tags:
                page_content = page_content + ' ' + h5.text

            b_tags = soup.body.findAll('b')
            for b in b_tags:
                page_content = page_content + ' ' + b.text

            span_tags = soup.body.findAll('span')
            for span in span_tags:
                page_content = page_content + ' ' + span.text

            i_tags = soup.body.findAll('i')
            for i in i_tags:
                page_content = page_content + ' ' + i.text

            p_tags = soup.body.findAll('p')
            for p in p_tags:
                page_content = page_content + ' ' + p.text

            page_content = striphtml(page_content)
            page_content = stripcomment(page_content)
            page_content = stripurl(page_content)

            if 'Page not found Contact Information' not in page_content and len(page_content>0):
                with open(relative_path + str(index) + '.txt', 'w') as f:
                    f.write(page_content)
                index = index + 1
                print(relative_path + 'finish writing to ' + str(index) + '.txt')

    except requests.exceptions.RequestException as e:
        print("error")
        pass

if __name__ == '__main__':
    # links_lst = []
    # get_links_within_page('http://cufa.net', links_lst)
    # extract_text('http://cufa.net/support-professor-louise-briand-faculty-representative-uqo-board-governors/')

    with open('output2.pickle', 'rb') as f:
        links = pickle.load(f)
        links = list(set(links))
    temp = links[2201:3000]
    index = 1000
    relative_path = 'archive/'
    for url in links:
        print('parsing:' + url)
        extract_text(url)
        if index >= 1500:
            break


# def printPickle():
#     filepath = 'links.pickle'
#     links = afinnreader.readList(filepath)
#     print(len(links))
#     for link in links:
#         print(link)
#         # afinnreader.saveList('links.pickle', links)
#
#
# # def crawling(start_url, count_limit):
# if __name__ == '__main__':
    # links_lst = []
    # links_lst = ['http://www.cupfa.org']
    # links_lst = recursive_get_link(links_lst, 0)
    # links_lst = read_list('output2.pickle')
    # print(len(links_lst))
    # for link in links_lst:
    #     print(link)
    # links = recursive_get_link(links_lst, 0)
    # printPickle()
