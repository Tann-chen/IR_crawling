from bs4 import BeautifulSoup
import requests


def get_links_within_page(url):
    global links_lst

    current_page_links = []

    try:
        response = requests.get(url, timeout=0.5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())
        a_tags = soup.findAll('a')

        for a in a_tags:
            link = a['href']
            if link[:4] == 'http' or link[:3] == 'www':
                current_page_links.append(link)
                links_lst.append(link)
            else:
                current_page_links.append(link)
                links_lst.append(url + link)  # relative path

    except requests.exceptions.RequestException as e:
        print('*** one exception in request for crawling page ***')
        print(str(e))

    return current_page_links


def crawling(start_url, depth):



if __name__ == '__main__':
    links_lst = []
    get_links_within_page('http://www.baidu.com')
