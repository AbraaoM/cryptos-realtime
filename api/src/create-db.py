import mysql.connector
from app import db as db_model

db = mysql.connector.connect(
  host='172.22.0.2',
  user='root',
  passwd='projetoCryptos'
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE crypto_data")

db_model.create_all()
