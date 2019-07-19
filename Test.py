import json
with open('youtube_credentials.json') as cred_data:
    info = json.load(cred_data)
    api_key = info["youtube_apikeyjson"]

    

from apiclient.discovery import build
youtube = build('youtube' , 'v3' , developerKey= api_key)

def commentsearch(videoIdentification, partofcomment = "snippet", numbrofresult = 100):
    print("Inside Comment Search...")
    callobject = youtube.commentThreads().list(part=partofcomment,videoId=videoIdentification,maxResults=numbrofresult,textFormat = "plainText")
    results = callobject.execute()
    totallist = []
	


    def incosearch():
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            resultdic = {"user" : author ,"usercomment" : comment["snippet"]["textDisplay"], 
                       "likecount" : comment["snippet"]["likeCount"], "commentid" : item["id"] ,
                         "publishingdate" : comment["snippet"]["publishedAt"] }
            totallist.append(resultdic)

    incosearch()


    if("nextPageToken" in results) == True:
        while ("nextPageToken" in results) == True :
            callobject = youtube.commentThreads().list(part = partofcomment, videoId = videoIdentification, maxResults = numbrofresult, 
                                               textFormat = "plainText", pageToken = results["nextPageToken"])
            results = callobject.execute()

            incosearch()

        print(len(totallist))

        return (totallist)

    elif ("nextPageToken" in results) == False :
        print(len(totallist))
        return(totallist)


def foo(id):
    print("Inside Foo....")
    comm = commentsearch(id)
    comm_list=[]
    for i in comm:
        comm_list.append(i['usercomment'])
    print("Comments Extracted...")
    print( compute(comm_list) )


import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import pickle


def compute(comm_list):
    print("Inside Compute...")
    df5 = pd.DataFrame(comm_list)
    df5.columns = ['text']
    print(df5)
    df5['text'] = df5['text'].str.lower()
    df5['text'] = df5['text'].str.replace('[^\w\s]','')
    df5['text'] = df5['text'].str.replace('\d+', '')
    df5.dropna(subset = ['text'], inplace=True )
    df5 = df5[~df5.isin([' ','  ']).any(axis = 1)]
    stop = set(stopwords.words('english'))
    ps = SnowballStemmer('english')
    df5['text'] = df5['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    ps = SnowballStemmer('english')
    df5['text'] = df5['text'].apply(lambda x : ' '.join( [ps.stem( word ) for word in x.split()] ))
    #vectoriser = CountVectorizer()
    #tf_idf_vectorizer = TfidfTransformer(use_idf = True)
    m_ = open('vectorizer_pickle', 'rb')
    s_ = pickle.load(m_)
    comm = df5['text'].tolist()
    #test = vectoriser.transform(comm)
    test = s_.transform(comm)
    #X_test = tf_idf_vectorizer.transform(test)
    #X_test = s_.transform(test)
    m = open('model_pickle', 'rb')
    s = pickle.load(m)
    res = s.predict(test)
    l = res.tolist()
    U = Counter(l)
    if U['Science'] + U['News'] > U['Comedy'] + U['TV']:
        return 1
    
    return 0

#Uncomment below line for testing Test.py separately,else remain commented for controller to work.
#foo('ncmUToEIpEA')



