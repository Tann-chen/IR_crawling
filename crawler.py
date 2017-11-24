from bs4 import BeautifulSoup
import requests
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
    x = recursive_get_link(page_links, i+1)
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
            if 'href' in a.attrs:
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


def printPickle():
    filepath = 'links.pickle'
    links = afinnreader.readList(filepath)
    print(len(links))
    for link in links:
        print(link)
    # afinnreader.saveList('links.pickle', links)

# def crawling(start_url, count_limit):
if __name__ == '__main__':
    # links_lst = []
    links_lst = ['https://www.concordia.ca/artsci/students/associations.html']
    # links_lst = recursive_get_link(links_lst, 0)
    # for link in links_lst:
    #     print(link)
    # links = recursive_get_link(links_lst, 0)
    printPickle()