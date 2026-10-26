
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv


# .env dosyasini yukle
load_dotenv()

# MySQL baglantisi
baglanti = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="ecommerce_analysis"
)

print("MySQL baglantisi basarili!")


# SQL dosyasini oku
sql_dosyasi = Path("sql/siparis_durum_analizi.sql")
sorgu = sql_dosyasi.read_text(encoding="utf-8")

# SQL sorgusunu calistir
cursor = baglanti.cursor()
cursor.execute(sorgu)

veriler = cursor.fetchall()

# Pandas DataFrame olustur
siparis_analizi = pd.DataFrame(
    veriler,
    columns=["order_status", "siparis_sayisi"]
)

print(siparis_analizi)

cursor.close()
baglanti.close()


plt.figure(figsize=(10, 6))

plt.bar(
    siparis_analizi["order_status"],
    siparis_analizi["siparis_sayisi"]
)

plt.title("Order Status Distribution")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)
plt.yscale("log")
plt.tight_layout()

plt.savefig("Figures/order_status_distribution.png")
plt.show()
