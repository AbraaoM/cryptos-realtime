from tokenize import Number
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:projetoCryptos@172.22.0.2/crypto_data'
db = SQLAlchemy(app)

class Cryptos(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  currency = db.Column(db.String(4))
  timeframe = db.Column(db.Integer)
  datetime = db.Column(db.DateTime)
  Open = db.Column(db.Float)
  Low = db.Column(db.Float)
  High = db.Column(db.Float)
  Close = db.Column(db.Float)

req: dict = requests.get('https://poloniex.com/public?command=returnTicker')

print(req.json()["USDC_BTC"])


