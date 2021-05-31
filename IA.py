##AQUI SE ENCUENTRAN LAS LIBRERIAS QUE DEBERAN DE SER INSTALADAS PARA PODER EJECUTAR EL PROYECTO
#pip install -U pip setuptools wheel
#pip install -U spacy
#python -m spacy download es_core_news_sm

import spacy
from spacy.matcher import Matcher
import tweepy
from tweepy import OAuthHandler
import json
import replaceall
from replaceall import replaceall
import requests
import matplotlib.pyplot as plt
import pandas as pd

import emoji
from matplotlib import colors
import matplotlib.pyplot as barra
import matplotlib.pyplot as pie


consumer_key = "Jv0DKLySkVhApn5wqWncwYdXA"
consumer_secret = "6l9mcrFK2LOqwtYLPv44f8lRouNErwRMf0amY1F9139qcoXyQB"
access_token = "1327697310852263936-iY1jE227HA8PReLGtdMjD5v2yj6IME"
access_token_secret = "zsl6wQjuOItu3MlUGpjjmQZVzYCJsUzynzWSEhMBpJS3P"
palabraClave = "veneco"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


nlp = spacy.load("es_core_news_sm")
matcher = Matcher(nlp.vocab)
xe = 0
noxe = 0
for tweet in tweepy.Cursor(api.search, palabraClave, tweet_mode="extended").items(1000): 
    twet = replaceall(tweet._json['full_text'],"[.;!?(){}\\[\\]<>%@,:0123456789#$/_-|¿...¡]").lower()
    doc = nlp(
        twet.lower()
    )

    pattern = [{"TEXT": {"IN": ["puto","puta"]}}, {"TEXT": {"IN":["veneco","veneca"]}}]
    pattern2 = [{"POS":"NOUN"}, {"POS":"AUX"}, {"POS":"DET"}, {"POS":"NOUN"}]
    pattern3 = [{"POS":"NOUN"}, {"POS":"VERB"}, {"POS":"DET"}, {"POS":"NOUN"}]
    pattern4 = [{"POS":"NOUN"}, {"POS":"AUX"}, {"POS":"ADJ"}]
    pattern5 = [{"POS":"VERB"}, {"POS":"ADP"}, {"POS":"DET"}, {"POS":"NOUN"}]
    pattern6 = [{"POS":"NOUN"}, {"POS":"ADJ"}]
    pattern7 = [{"POS":"VERB"},{"TEXT":"asco"}]
    pattern8 = [{"TEXT":{"IN":["venezolanos", "venezolanas"]}}]
    pattern9 = [{"TEXT":{"IN":["venecos", "venecas"]}}]

    pattern10 = [{"TEXT":{"IN":["imbesiles", "imbesil", "lacayos", "homofobicos", "lacayo", "homofobico","marico","marica","maricos","maricas"]}}]

    # Añade el patrón al matcher y usa el matcher sobre el documento
    matcher.add("NOUN_ADJ_PATTERN", [pattern,pattern2,pattern3,pattern4,pattern5,pattern6,pattern7,pattern8,pattern9,pattern10])
    matches = matcher(doc)
    #print("Total de resultados encontrados:", len(matches), "de", len(doc))

    promedio = 0

    # Itera sobre los resultados e imprime el texto del span
    for match_id, start, end in matches:
        promedio = promedio + (end-start)
        #print("Resultado encontrado:", doc[start:end].text)
        
    #print("Promedio: ",  promedio/len(doc) )   
    if(len(matches) >= 2):
        print("texto Xenofobico :/\n", "Promedio: ",len(matches), "\nTweet:" ,twet,"\n" )
        xe = xe +1
    else:
        print("Texto NO Xenofobico C:\n", "Promedio: ",len(matches), "\nTweet:" ,twet,"\n" )
        noxe = noxe +1


pizza = ("Xenofobico","No Xenofobico")
ventas = (xe, noxe)
colores = ("red", "green")

barra.title("Xenofobia en twitter")
barra.bar(pizza, height = ventas, color = colores, width = 0.5)
barra.show()

barra.title("Xenofobia en twitter")
barra.pie(ventas, colors=colores, labels=pizza, autopct=("%1.f%%"))
barra.show()
