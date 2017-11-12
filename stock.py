import requests
import sys
import numpy as np
import tweepy
import os

from keras.models import Sequential
from keras.layers import Dense
from textblob import TextBlob

global user
consumer_key = "lMikOtj0ma5TIHpA19RwtOI4I"
comsumer_secret = "l0BEwFO5Uf3n7r5jsixQdXa1Q3yGahECJfzQkeLwkdosXmQEAo"
access_token = "707193271085195264-3hUR2RQjrimKiK9QuSRjg0DLYk8LiAe"
access_secret = "IL44riluYZQrLMbkFuTc2dVY0tDVIewgr7kghQLqSvKrZ"
login = tweepy.OAuthHandler(consumer_key, comsumer_secret)
login.set_access_token(access_token, access_secret)
user = tweepy.API(login)

file = 'historical.csv'


def get_name(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


def sentiment(quote, num,user):
    tweet_list = user.search(get_name(quote), count=num)
    positive = 0
    null = 0
    for tweet in tweet_list:
        check = TextBlob(tweet.text).sentiment
        if check.subjectivity == 0:
            null += 1
            next
        if check.polarity > 0:
            positive += 1

    return positive / (num - null)


def get_data(quote):
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A' + quote + '&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(file, 'wb') as fl:
            for line in r:
                fl.write(line)
    return True


def predict():
    data = []
    with open(file) as f:
        for num, line in enumerate(f):
            if num != 0:
                data.append(float(line.split(',')[1]))
    data = np.array(data)

    def create_set(data):
        datax = [data[n + 1] for n in range(len(data) - 2)]
        return np.array(datax), data[2:]

    trainx, trainy = create_set(data)

    classifier = Sequential()
    classifier.add(Dense(8, input_dim=1, activation='relu'))
    classifier.add(Dense(1))
    classifier.compile(loss='mean_squared_error', optimizer='adam')
    classifier.fit(trainx, trainy, nb_epoch=80, batch_size=20, verbose=2)

    prediction = classifier.predict(np.array([data[0]]))
    return '%s %s' % (data[0], prediction[0][0])


def modulus(x):
    if x >= 0:
        return x
    return (-1 * x)

def callback(quote):
    #quote = input('Enter stock quote: ').upper()
    quote=quote.upper()
    if not get_data(quote):
        print ('ERROR, please re-run the script')

    values_str = predict()
    valueList = values_str.split()
    data_value = float(valueList[0])
    pred_value = float(valueList[1])

    print('Sentiment Score of the company is: (0.00  being very bad and 1.00  being very good)')
    score = sentiment(quote, 400, user)
    print('Sentiment score: ', score)

    if score >= 0.5:
        pred_value = pred_value + (modulus(data_value - pred_value) * 0.1 * (pow(5, modulus(0.5 - score)) - 1))
    else:
        pred_value = pred_value - (modulus(data_value - pred_value) * 0.1 * (pow(5, modulus(0.5 - score)) - 1))

    print('From ' + str(data_value) + ' to ' + str(pred_value))

    return (score,data_value,pred_value,quote)
    # os.remove(file)