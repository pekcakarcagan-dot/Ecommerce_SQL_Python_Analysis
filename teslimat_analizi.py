import matplotlib.pyplot as plt
import os 
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
baglanti = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="ecommerce_analysis"
)

print("MySQL baglantisi basarili!")

# SQL sorgusu
sorgu = """
SELECT
    CASE
        WHEN order_delivered_customer_date >
             order_estimated_delivery_date
        THEN "Gecikti"
        ELSE "Zamanında"
    END AS teslimat_durumu,
    COUNT(*) AS siparis_sayisi
FROM orders
WHERE order_status="delivered"
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL
GROUP BY teslimat_durumu;
"""
# SQL sorgusunu calistir
cursor = baglanti.cursor()
cursor.execute(sorgu)
# Sonuclari al
veriler= cursor.fetchall()
#Pandas tablosu oluştur
teslimat_df=pd.DataFrame(
 veriler,
 columns=["teslimat_durumu","siparis_sayisi"]
)
print(teslimat_df)
cursor.close()
baglanti.close()

# Teslimat performansı grafiği
plt.figure(figsize=(8,8))

plt.pie(
    teslimat_df["siparis_sayisi"],
    labels=teslimat_df["teslimat_durumu"],
    autopct="%1.2f%%",
    startangle=90
)
plt.title("Delivery Performance Analysis")
plt.tight_layout()
plt.savefig(
    "Figures/delivery_performance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
