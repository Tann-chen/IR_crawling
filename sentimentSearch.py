import pickle

def getSentiment(queries, docList):
    global index
    sentiment_query = 0

    queries = [x.lower() for x in queries]
    for query in queries:
        if query in index:
            sentiment_query = sentiment_query + int(index[query]['sentiment'])
            index[query].pop('sentiment')
            docList[query] = index[query]
    return sentiment_query

if __name__ == '__main__':
    docList = {}
    x = 'good job'
    with open('inverted_index.pickle', 'rb') as f_1:
        index = pickle.load(f_1)
    queries = x.split(" ")
    # 这个是query的sentiment value
    sentimentValue = getSentiment(queries, docList)
    print('sentimentValue = '+str(sentimentValue))
    # docList 里面是所有相关doc的, run 一下就能看到
    print(docList)