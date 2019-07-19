import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import pickle

df = pd.read_csv("YOUR_LOCATION\\comments_PewDiePie.csv")
df.drop(['videoId','commentId','author','replies','likes','publishedAt'],axis=1,inplace=True)
df['Category'] = 'Comedy'

df1 = pd.read_csv("YOUR_LOCATION\\comments_ScienceChannel.csv")
df1.drop(['videoId','commentId','author','replies','likes','publishedAt'],axis=1,inplace=True)
df1['Category'] = 'Science'
#print(df1.head())

df2 = pd.read_csv("YOUR_LOCATION\\comments_Corden.csv")
df2.drop(['videoId','commentId','author','replies','likes','publishedAt'],axis=1,inplace=True)
df2['Category'] = 'TV'

df3 = pd.read_csv("YOUR_LOCATION\\comments_TYT.csv")
df3.drop(['videoId','commentId','author','replies','likes','publishedAt'],axis=1,inplace=True)
df3['Category'] = 'News'

df4 = pd.read_csv("YOUR_LOCATION\\comments_SciShow.csv")
df4.drop(['videoId','commentId','author','replies','likes','publishedAt'],axis=1,inplace=True)
df4['Category'] = 'Science'

df4 = df4[1: 9202]

result1 = df.append(df1,ignore_index=True)
result2 = df2.append(df3, ignore_index=True)
result3 = result1.append(result2, ignore_index=True)
result4 = result3.append(df4, ignore_index=True)
print("Values Count: "+str(result4['Category'].value_counts()))

result4['text']=result4['text'].str.lower()
result4['text'] = result4['text'].str.replace('[^\w\s]','')
result4.head()
result4['text'] = result4['text'].str.replace('\d+', '')
result4.dropna(subset = ['text'], inplace=True )
result4 = result4[~result4.isin([' ','  ']).any(axis = 1)]

stop = set(stopwords.words('english'))
result4['text'] = result4['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
ps = SnowballStemmer('english')
result4['text'] = result4['text'].apply(lambda x : ' '.join( [ps.stem( word ) for word in x.split()] ))
ps = SnowballStemmer('english')

vectoriser = CountVectorizer()
tf_idf_vectorizer = TfidfTransformer(use_idf = True)

comment = result4['text'].tolist()
y_train = result4.iloc[:,1].values

X = vectoriser.fit_transform(comment)
print(X)
X_Train = tf_idf_vectorizer.fit_transform(X)
print(X_Train)
with open('vectorizer_pickle', 'wb') as file:
	pickle.dump(vectoriser, file)
	print("done vectoriser")


clf1 = RandomForestClassifier()
clf1.fit(X_Train,y_train)

with open('model_pickle', 'wb') as file:
	pickle.dump(clf1, file)
	print("Done model")
