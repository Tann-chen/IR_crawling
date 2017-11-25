from bs4 import BeautifulSoup

if __name__ == '__main__':
    tttt = '<head>hhh</head><body>body<a>aaabody</a></body><footer>xixixix<a>aaafooter</a></footer>'
    soup = BeautifulSoup(tttt, 'html.parser')
    a_tags = soup.body.findAll('a')
    for a in a_tags:
        print(a.text)




