from bs4 import BeautifulSoup
import requests
import re
import os
import afinnreader

threshold = 1


def recursive_get_link(links, i):
    global rootdir
    global file
    file = 'output2.pickle'

    afinnreader.saveList(file, links)
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
        response = requests.get(url)
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


def extract_text(target_url):
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    page_content = ''

    h1_tags = soup.findAll('h1')
    for h1 in h1_tags:
        page_content = page_content + ' ' + h1.text

    h2_tags = soup.findAll('h2')
    for h2 in h2_tags:
        page_content = page_content + ' ' + h2.text

    h3_tags = soup.findAll('h3')
    for h3 in h3_tags:
        page_content = page_content + ' ' + h3.text

    h4_tags = soup.findAll('h4')
    for h4 in h4_tags:
        page_content = page_content + ' ' + h4.text

    h5_tags = soup.findAll('h5')
    for h5 in h5_tags:
        page_content = page_content + ' ' + h5.text

    b_tags = soup.findAll('b')
    for b in b_tags:
        page_content = page_content + ' ' + b.text

    span_tags = soup.findAll('span')
    for span in span_tags:
        page_content = page_content + ' ' + span.text

    i_tags = soup.findAll('i')
    for i in i_tags:
        page_content = page_content + ' ' + i.text

    p_tags = soup.findAll('p')
    for p in p_tags:
        page_content = page_content + ' ' + p.text

    page_content = striphtml(page_content)
    page_content = stripcomment(page_content)

    print(page_content)
    return page_content


# if __name__ == '__main__':
    # links_lst = []
    # get_links_within_page('http://cufa.net', links_lst)
    # extract_text('http://cufa.net/support-professor-louise-briand-faculty-representative-uqo-board-governors/')


def printPickle():
    filepath = 'links.pickle'
    links = afinnreader.readList(filepath)
    print(len(links))
    for link in links:
        print(link)
        # afinnreader.saveList('links.pickle', links)


# def crawling(start_url, count_limit):
if __name__ == '__main__':
    links = afinnreader.readList('links.pickle')
    for link in links:
        extract_text(link)

    # links_lst = []
    # links_lst = ['https://www.concordia.ca/artsci/students/associations.html']
    # links_lst = recursive_get_link(links_lst, 0)
    # for link in links_lst:
    #     print(link)
    # links = recursive_get_link(links_lst, 0)
    # printPickle()
