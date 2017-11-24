from bs4 import BeautifulSoup
import requests


def get_links_within_page(url, links_container):
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
                        current_page_links.append(link)
                        links_container.append(link)
                    else:
                        current_page_links.append(link)
                        links_container.append(url + link)  # relative path

    except requests.exceptions.RequestException as e:
        print('*** one exception in request for crawling page ***')
        print(str(e))

    return


# def crawling(start_url, count_limit):


if __name__ == '__main__':
    links_lst = []
    get_links_within_page('https://csu.qc.ca/content/student-groups-associations', links_lst)

    for link in links_lst:
        print(link)
