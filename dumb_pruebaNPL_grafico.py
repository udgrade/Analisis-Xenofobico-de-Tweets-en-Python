##AQUI SE ENCUENTRAN LAS LIBRERIAS QUE DEBERAN DE SER INSTALADAS PARA PODER EJECUTAR EL PROYECTO

#pip install tweepy
#pip install replaceall
#pip install pycorenlp
#pip install numpy
#pip install matplotlib
#pip install pandas
#pip install emoji

#SE DEBERA DE UTILIZAR EL SIGUIENTE COMANDO PARA PONER EN MARCHAR LA LIBRERIA DE StanfordCoreNLP QUE SE ENCUENTRA ESCRITA EN JAVA
#biblioteca (Se encuentra en la carpeta local del proyecto - stanford-corenlp)
#java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

import tweepy
from tweepy import OAuthHandler
import json
import replaceall
from replaceall import replaceall
from pycorenlp import StanfordCoreNLP
import requests
import matplotlib.pyplot as plt
import pandas as pd

import emoji


nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
palabraClave = "veneco"
contNeu = 0
contNeg = 0 
contPos = 0

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, palabraClave, tweet_mode="extended").items(100): 
    print (replaceall(tweet._json['full_text'],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]"))
    doc = replaceall(tweet._json['full_text'],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]")
    doc = emoji.get_emoji_regexp().sub(r'', doc)
    annot_doc = json.loads(nlp_wrapper.annotate(doc,properties={'annotators': 'sentiment',
                                                                'outputFormat': 'json',
                                                                'timeout': 100000,}))
    for sentence in annot_doc["sentences"]:
        print (str(sentence["sentimentValue"]) + " = "+ sentence["sentiment"] + '\n')

        if (sentence["sentiment"] == 'Neutral') : 
            contNeu = contNeu+1
        elif (sentence["sentiment"] == 'Negative') :
            contNeg = contNeg+1
        elif (sentence["sentiment"] == 'Positive') :
            contPos = contPos+1

print('Los valores resultantes fueron -contNeu: '+str(contNeu)+', -contNeg: '+str(contNeg)+', -contPos: '+str(contPos))

#Grafico Circular
labels = 'Neutral', 'Negativos', 'Positivos'
sizes = [contNeu, contNeg, contPos]
explode = (0.1, 0, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.show()

#Generacion de Histograma
plt.style.use('fivethirtyeight')

List = []
for i in range(contNeu):
    List.append('1')
for j in range(contNeg):
    List.append('2')
for q in range(contPos):
    List.append('3')
#print(List)    

ages = List

plt.hist(ages, bins=3, edgecolor='black')

plt.title('Medicion de Sentimientos')
plt.xlabel('Tweets 1. Neutrales, 2. Negaticos y 3. Positivos')
plt.ylabel('Cantidad de Tweets')

plt.tight_layout()

plt.show()

##Grafico Plot
m = [1,2,3]
n = [contNeu, contNeg, contPos]

plt.title('Medicion de Sentimientos')
plt.xlabel('Tweets 1. Neutrales, 2. Negaticos y 3. Positivos')
plt.ylabel('Cantidad de Tweets')

plt.plot(m,n)
plt.show()
