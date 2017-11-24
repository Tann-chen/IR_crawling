import requests
from bs4 import BeautifulSoup
import urllib

def get_content(url):

    response = requests.get(url, timeout=10)
    print(response.text)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # # print(soup.prettify())
    # a_tags = soup.findAll('p')
    #
    # return a_tags

if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/19962262'
    # html = getHtml("https://csu.qc.ca/content/student-groups-associations")
    content_list = get_content(url)
    # for paragraph in content_list:
    #     print(paragraph)