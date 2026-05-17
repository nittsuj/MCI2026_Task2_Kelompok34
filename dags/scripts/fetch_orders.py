"""
Task 1: tarik data orders dari API, ratakan strukturnya, lalu simpan ke data lake.

API mengembalikan JSON dengan bentuk:
{ total_orders, orders: [...] }

Setiap order memiliki array products, sehingga data di-flatten menjadi satu baris
per pasangan (order, product) agar mudah diolah pada tahap agregasi Spark.
"""

import os
from datetime import datetime

import pandas as pd
import requests


API_URL = "http://96.9.212.102:8000/orders"


def fetch_orders():
    print(f"Menarik orders dari {API_URL}...")

    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        print(f"Gagal menarik data: {exc}")
        raise

    orders = payload.get("orders", [])
    print(f"Dapat {len(orders)} orders dari API")

    rows = []
    for order in orders:
        order_id = order.get("order_id")
        user_id = order.get("user_id")
        order_dow = order.get("order_dow")
        order_hour = order.get("order_hour_of_day")

        for product in order.get("products", []):
            rows.append(
                {
                    "order_id": order_id,
                    "user_id": user_id,
                    "order_dow": order_dow,
                    "order_hour": order_hour,
                    "product_id": product.get("product_id"),
                    "product_name": product.get("product_name"),
                    "aisle": product.get("aisle"),
                    "department": product.get("department"),
                    "add_to_cart_order": product.get("add_to_cart_order"),
                    "reordered": product.get("reordered", 0),
                }
            )

    if not rows:
        print("Tidak ada product line yang berhasil diekstrak. Proses simpan dilewati.")
        return

    df = pd.DataFrame(rows)
    print(f"Flatten selesai: {len(df)} baris order-product")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"/opt/airflow/data_lake/orders/orders_{stamp}.parquet"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)

    print(f"Data parquet tersimpan di {output_path}")


if __name__ == "__main__":
    fetch_orders()
