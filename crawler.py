from bs4 import BeautifulSoup
import requests

threshold = 1


def recursive_get_link(links, i):
    if i > threshold:
        return
    page_links = []
    for link in links:
        new_page_links = get_links_within_page(link)
        page_links += new_page_links
    return_page_links = recursive_get_link(page_links, i+1)

    return recursive_get_link()


def get_links_within_page(url):
    global links_lst

    current_page_links = []

    try:
        response = requests.get(url, timeout=10)
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


if __name__ == '__main__':
    links_lst = ['http://www.baidu.com']
    links_lst = get_links_within_page('https://www.google.ca/?gfe_rd=cr&dcr=0&ei=YncXWvGsEu6BX8XKryA')
    # links_lst = recursive_get_link(links_lst, 0)
    for link in links_lst:
        print(link)