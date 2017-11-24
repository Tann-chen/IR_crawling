from bs4 import BeautifulSoup
import requests
import re


def get_links_within_page(url, links_container):
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
                        current_page_links.append(link)
                        links_container.append(link)
                    else:
                        current_page_links.append(link)
                        links_container.append(url + link)  # relative path

    except requests.exceptions.RequestException as e:
        print('*** one exception in request for crawling page ***')
        print(str(e))


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


if __name__ == '__main__':
    # links_lst = []
    # get_links_within_page('http://cufa.net', links_lst)
    extract_text('http://cufa.net/support-professor-louise-briand-faculty-representative-uqo-board-governors/')
