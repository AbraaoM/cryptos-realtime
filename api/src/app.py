from tokenize import Number
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
from pytz import timezone
import time
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:projetoCryptos@172.22.0.2/crypto_data'
db = SQLAlchemy(app)

# Model para a criação da tabela que armazenará os dados necessários no banco de dados
class Cryptos(db.Model):
  id: int = db.Column(db.Integer, primary_key = True)
  currency: str = db.Column(db.String(10))
  timeframe: int = db.Column(db.Integer)
  datetime:int = db.Column(db.DateTime)
  Open: float = db.Column(db.Float)
  Low: float = db.Column(db.Float)
  High: float = db.Column(db.Float)
  Close: float = db.Column(db.Float)

# Cria as estruturas que montarão o candle vigente nos timeframes de 
# 1, 5 e 10 minutos
candle1min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
candle5min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
candle10min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}

def GetCurrency(symbol):
  try:
    response = requests.get('https://poloniex.com/public?command=returnTicker')
    response.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print(errh)
  except requests.exceptions.ConnectionError as errc:
    print(errc)
  except requests.exceptions.Timeout as errt:
    print(errt)
  except requests.exceptions.RequestException as err:
    print(err)
  finally:
    return response.json()[symbol]



# Processa as informações trazidas da API da Poloniex 
# organizando o maior preço para 1 minuto
def Set1minHigh(lastPrice: float):
  if candle1min['high'] < lastPrice:
    candle1min['high'] = lastPrice

# Processa as informações trazidas da API da Poloniex 
# organizando o menor preço para 1 minuto
def Set1minLow(lastPrice: float):
  if candle1min['low'] > lastPrice or candle1min['low'] == 0:
    candle1min['low'] = lastPrice

# Processa as informações trazidas da API da Poloniex 
# organizando o preço de abertura para 1 minuto.
# Limpa o dicionário que armazena dados do candle para
# que novas informações sejam adicioonadas.
def open1min(lastPrice: float):
  global candle1min
  candle1min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
  candle1min['open'] = lastPrice

# Processa as informações trazidas da API da Poloniex 
# organizando o preço de fechamento para 1 minuto.
# Insere os dados do último candle fechado no banco de dados.
def close1min(lastPrice: float):
  candle1min['close'] = lastPrice

  try:
    crypto1min = Cryptos(currency= currencySymbol, 
                      timeframe= 1, 
                      datetime= datetime.now(timezone('america/sao_paulo')), 
                      Open= candle1min['open'],
                      Low= candle1min['low'],
                      High= candle1min['high'],
                      Close= candle1min['close'])
    db.session.add(crypto1min)
    db.session.commit()
  except Exception as ex:
    print(ex)


def Set5minHigh(lastPrice: float):
  if candle5min['high'] < lastPrice:
    candle5min['high'] = lastPrice

def Set5minLow(lastPrice: float):
  if candle5min['low'] > lastPrice or candle5min['low'] == 0:
    candle5min['low'] = lastPrice

def open5min(lastPrice: float):
  global candle5min
  candle5min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
  candle5min['open'] = lastPrice

def close5min(lastPrice: float):
  candle5min['close'] = lastPrice

  try:
    crypto5min = Cryptos(currency= currencySymbol, 
                      timeframe= 5, 
                      datetime= datetime.now(timezone('america/sao_paulo')), 
                      Open= candle5min['open'],
                      Low= candle5min['low'],
                      High= candle5min['high'],
                      Close= candle5min['close'])
    db.session.add(crypto5min)
    db.session.commit()
  except Exception as ex:
    print(ex)


def Set10minHigh(lastPrice: float):
  if candle10min['high'] < lastPrice:
    candle10min['high'] = lastPrice

def Set10minLow(lastPrice: float):
  if candle10min['low'] > lastPrice or candle10min['low'] == 0:
    candle10min['low'] = lastPrice

def open10min(lastPrice: float):
  global candle10min
  candle10min = {'open': 0.0, 'low': 0.0, 'high': 0.0, 'close': 0.0}
  candle10min['open'] = lastPrice

def close10min(lastPrice: float):
  candle10min['close'] = lastPrice

  try:
    crypto10min = Cryptos(currency= currencySymbol, 
                      timeframe= 10, 
                      datetime= datetime.now(timezone('america/sao_paulo')), 
                      Open= candle10min['open'],
                      Low= candle10min['low'],
                      High= candle10min['high'],
                      Close= candle10min['close'])
    db.session.add(crypto10min)
    db.session.commit()
  except Exception as ex:
    print(ex)


# Cria um loop infinito para acesso constante aos dados 
# trazidos da Poloniex, processamento e alimentação do banco de dados.
# O loop é executado uma vez por segundo.
currencySymbol: str = sys.argv[1]
while True:
  currency = GetCurrency(currencySymbol)

  currentTime = datetime.now(timezone('america/sao_paulo')).time()
  datetime.now()
  Set1minHigh(float(currency['last']))
  Set1minLow(float(currency['last']))

  Set5minHigh(float(currency['last']))
  Set5minLow(float(currency['last']))

  Set10minHigh(float(currency['last']))
  Set10minLow(float(currency['last']))

  if currentTime.second == 0:
    open1min(currency['last'])
  elif currentTime.second == 59:
    close1min(currency['last'])

  index = 1 if len(str(currentTime.minute)) > 1 else 0
  if currentTime.minute % 5 == 0 and currentTime.second == 0:
    open5min(currency['last'])
  elif (str(currentTime.minute)[index] == '4' or str(currentTime.minute)[index] == '9') and currentTime.second == 59:
    close5min(currency['last'])

  if currentTime.minute % 10 == 0 and currentTime.second == 0:
    open10min(currency['last'])
  elif (str(currentTime.minute)[index] == '4' or str(currentTime.minute)[index] == '9') and currentTime.second == 59:
    close10min(currency['last'])
  time.sleep(1)
