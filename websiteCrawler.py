from bs4 import BeautifulSoup
import os
import urllib


def parse(filepointer):
    soup = BeautifulSoup(filepointer, 'html.parser')
    links = soup.find_all('a')
    print links
    # for link in soup.find_all('a'):
    #     print link.name, link['href']


#coding=utf-8

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


if __name__ == '__main__':
    html = getHtml("https://csu.qc.ca/content/student-groups-associations")
    print html
    # parse(html)