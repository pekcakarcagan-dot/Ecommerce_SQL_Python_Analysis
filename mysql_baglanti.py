
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

baglanti = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="ecommerce_analysis"
)


print("MYSQL bağlantısı başarılı!")
import pandas as pd
sorgu = """
SELECT
    c.customer_city,
COUNT(o.order_id) AS toplam_siparis
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_city
ORDER BY toplam_siparis DESC
LIMIT 10;

"""
cursor=baglanti.cursor()
cursor.execute(sorgu)
veriler=cursor.fetchall()
sehir_analizi=pd.DataFrame(
    veriler,
    columns=["customer_city","toplam_siparis"]
)
print(sehir_analizi)
import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.bar(
    sehir_analizi["customer_city"],
    sehir_analizi["toplam_siparis"]
)
plt.title("Most Ordered 10 City")
plt.xlabel("Cities")
plt.ylabel("Order Number")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()



cursor.close()
baglanti.close()