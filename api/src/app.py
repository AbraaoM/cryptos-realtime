from tokenize import Number
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import requests
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:projetoCryptos@172.22.0.2/crypto_data'
db = SQLAlchemy(app)

class Cryptos(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  currency = db.Column(db.String(10))
  timeframe = db.Column(db.Integer)
  datetime = db.Column(db.DateTime)
  Open = db.Column(db.Float)
  Low = db.Column(db.Float)
  High = db.Column(db.Float)
  Close = db.Column(db.Float)


candle1min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}

high: float = 0
low: float = 0


def GetCurrency(symbol):
  req = requests.get('https://poloniex.com/public?command=returnTicker')
  return req.json()[symbol]

def Set1minHigh(lastPrice: float):
  if candle1min['high'] < lastPrice:
    candle1min['high'] = lastPrice

def Set1minLow(lastPrice: float):
  if candle1min['low'] > lastPrice or candle1min['low'] == 0:
    candle1min['low'] = lastPrice

def open1min(lastPrice: float):
  global candle1min
  candle1min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
  candle1min['open'] = lastPrice

def close1min(lastPrice: float):
  candle1min['close'] = lastPrice

  try:
    crypto = Cryptos(currency= "USDC_BTC", 
                      timeframe= 1, 
                      datetime= datetime.datetime.now(), 
                      Open= candle1min['open'],
                      Low= candle1min['low'],
                      High= candle1min['high'],
                      Close= candle1min['close'])
    db.session.add(crypto)
    db.session.commit()
  finally:
    print("foi")




# currency = GetCurrency("USDC_BTC")
# SetHigh(float(currency["last"]))
# SetcurrentLow(float(currency["last"]))

# print(high)

while True:
  currency = GetCurrency("USDC_BTC")

  currentTime = datetime.datetime.now().time()

  Set1minHigh(float(currency['last']))
  Set1minLow(float(currency['last']))

  if currentTime.second == 0:
    open1min(currency['last'])
  if currentTime.second == 59:
    close1min(currency['last'])

  # if currentTime.minute % 5 == 0:
  #   open5min()
  # if (str(currentTime.minute)[1] == 4 or str(currentTime.minute)[1] == 9) and currentTime.second == 59:
  #   close5min()

  # if currentTime.minute % 10 == 0:
  #   open10min()
  # if (str(currentTime.minute)[1] == 4 or str(currentTime.minute)[1] == 9) and currentTime.second == 59:
  #   close10min()
  # if oneMinute()


