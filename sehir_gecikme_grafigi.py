
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# .env dosyasindaki bilgileri yukle
load_dotenv()

# MySQL veritabanina baglan
baglanti = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="ecommerce_analysis"
)

print("MySQL baglantisi basarili!")


# Sehirlerin gecikme oranlarini hesapla
sorgu = """
SELECT
    c.customer_city AS sehir,
    COUNT(*) AS toplam_teslimat,
    SUM(
        CASE
            WHEN o.order_delivered_customer_date >
                 o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS geciken_siparis,
    ROUND(
        SUM(
            CASE
                WHEN o.order_delivered_customer_date >
                     o.order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS gecikme_orani
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  AND c.customer_city IN ('sao paulo', 'maceio')
GROUP BY c.customer_city
ORDER BY geciken_siparis DESC;
"""

cursor = baglanti.cursor()
cursor.execute(sorgu)

veriler = cursor.fetchall()

sehir_df = pd.DataFrame(
    veriler,
    columns=[
        "sehir",
        "toplam_teslimat",
        "geciken_siparis",
        "gecikme_orani"
    ]
)

print(sehir_df)

cursor.close()
baglanti.close()


# Sehirlerin gecikme oranlarini gorsellestir
plt.figure(figsize=(8,5))


sutunlar = plt.bar(
    sehir_df["sehir"],
    sehir_df["gecikme_orani"],
    color=["steelblue", "orange"]
)

plt.bar_label(
    sutunlar,
    fmt="%.2f%%",
    padding=3
)


plt.title("City Delivery Delay Rates")
plt.xlabel("City")
plt.ylabel("Delay Rate (%)")

plt.tight_layout()
plt.savefig(
"Figures/city_delay_rates.png",
dpi=300,
bbox_inches="tight"
)
plt.show()

# BUSINESS INSIGHTS
# Sao Paulo:
# 15045 teslimatin 942'si gecikmistir.
# Gecikme orani: %6.26
#
# Maceio:
# 236 teslimatin 70'i gecikmistir.
# Gecikme orani: %29.66
#
# Sonuc:
# Sao Paulo'da geciken siparis sayisi daha yuksektir.
# Ancak Maceio'da gecikme orani daha yuksektir.
# Bu nedenle iki sehir farkli acilardan incelenmelidir.
