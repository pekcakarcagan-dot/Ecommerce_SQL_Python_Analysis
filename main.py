print("E-Ticaret SQL ve Phyton Analizi Başlıyor")
import pandas as pd
musteriler= pd.read_csv("data/olist_customers_dataset.csv")
print(musteriler.head())

print("Muşteri tablosunun boyutu:")
print(musteriler.shape)

print( "Sütun İsimleri:")
print(musteriler.columns)

print("Eksik veri sayıları:")
print(musteriler.isnull().sum())

import sqlite3
baglanti= sqlite3.connect("ecommerce.db")
musteriler.to_sql(
    "customers",
    baglanti,
    if_exists="replace",
    index=False

)
print("Müşteri tablosu SQL veritabanına aktarıldı!")
baglanti.close()


baglanti = sqlite3.connect("ecommerce.db")

sorgu = """
SELECT *
FROM customers
LIMIT 5;
"""
sonuc = pd.read_sql_query(sorgu, baglanti)
print(sonuc)
baglanti.close()
