from bs4 import BeautifulSoup

if __name__ == '__main__':
    tttt = '<head>hhh</head>body<a>aaabody</a><<footer>xixixix<a>aaafooter</a></footer>'
    soup = BeautifulSoup(tttt, 'html.parser')
    # a_tags = soup.body.findAll('h1')
    print(len(soup.findAll('body')))
    # for a in a_tags:
    #     print(a.text)




