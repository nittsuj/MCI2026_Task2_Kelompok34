"""
Task 2: baca file parquet dari data lake, agregasi metrik per produk,
lalu muat hasilnya ke ClickHouse. File parquet yang sudah diproses akan dibersihkan.
"""

import glob
import os

from clickhouse_driver import Client
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def run_spark_analytics():
    spark = (
        SparkSession.builder.appName("Orders_Products_Analytics")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )

    print("Membaca data parquet dari data lake...")
    df_raw = spark.read.parquet("file:///opt/airflow/data_lake/orders/")

    print("Mengagregasi seluruh produk pada snapshot terbaru...")
    all_products = (
        df_raw.groupBy("product_name", "department")
        .agg(
            F.count("*").alias("total_orders"),
            F.sum("reordered").alias("reorder_count"),
            F.countDistinct("user_id").alias("unique_users"),
        )
        .orderBy(F.desc("total_orders"))
    )

    final_results = all_products.toPandas()
    spark.stop()

    print(f"Memuat {len(final_results)} produk ke ClickHouse...")
    client = Client(host="clickhouse-server", user="admin", password="rahasia")

    client.execute("CREATE DATABASE IF NOT EXISTS analytics")
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics.orders_top_products (
            product_name String,
            department String,
            total_orders Int32,
            reorder_count Int32,
            unique_users Int32
        ) ENGINE = MergeTree()
        ORDER BY total_orders
        """
    )

    client.execute("TRUNCATE TABLE analytics.orders_top_products")
    data_tuples = [tuple(row) for row in final_results.to_numpy()]
    if data_tuples:
        client.execute("INSERT INTO analytics.orders_top_products VALUES", data_tuples)

    print("Membersihkan file parquet yang sudah diproses...")
    files = glob.glob("/opt/airflow/data_lake/orders/*.parquet")
    for file_path in files:
        try:
            os.remove(file_path)
        except OSError as exc:
            print(f"Gagal menghapus {file_path}: {exc.strerror}")

    print(f"Pipeline selesai. {len(data_tuples)} produk tersimpan di ClickHouse.")


if __name__ == "__main__":
    run_spark_analytics()
