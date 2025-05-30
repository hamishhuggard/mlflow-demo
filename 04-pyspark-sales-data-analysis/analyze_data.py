from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql.functions import col, sum as spark_sum, count, desc, to_timestamp, lit
import os

spark = SparkSession.builder \
        .appName("ComplexSalesAnalysis") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", 2) \
        .getOrCreate()

schema = StructType([
    StructField("TransactionID", StringType(), True),
    StructField("ProductID", StringType(), True),
    StructField("ProductName", StringType(), True),
    StructField("Quantity", StringType(), True), # read as string initially for cleaning
    StructField("Price", StringType(), True),
    StructField("TransactionDate", StringType(), True),
])

output_dir = "spark_output"
sales_data_file = os.path.join(output_dir, "sales_transactions.csv")

print("Reading sales data...")
df = spark.read \
        .option("header", "true") \
        .schema(schema) \
        .csv(sales_data_file)

df.printSchema()
df.show(5)

print("Rows: {df.count()}")

print("Performing data cleaning and type casting...")

cleaned_df = df \
        .filter(col("TransactionID").isNotNull()) \
        .filter(col("ProductID").isNotNull()) \
        .filter(col("ProductName").isNotNull()) \
        .withColumn("Quantity_Parsed", col("Quantity").try_cast(IntegerType())) \
        .withColumn("Price_Parsed", col("Price").try_cast(DoubleType())) \
        .withColumn("TransactionDate_Parsed", to_timestamp(col("TransactionDate"), "yyyy-MM-dd HH:mm:ss")) \
        .filter(col("Quantity_Parsed").isNotNull()) \
        .filter(col("Price_Parsed").isNotNull()) \
        .filter(col("TransactionDate_Parsed").isNotNull()) \
        .withColumn("TotalSale", col("Quantity_Parsed") * col("Price_Parsed")) \
        .select(
            col("TransactionID"),
            col("ProductID"),
            col("ProductName"),
            col("Quantity_Parsed").alias("Quantity"),
            col("Price_Parsed").alias("Price"),
            col("TransactionDate_Parsed").alias("TransactionDate"),
            col("TotalSale")
        )

print("Cleaned schema:")
cleaned_df.printSchema()
print("Head:")
cleaned_df.show(5)
print("Rows after cleaning: {cleaned_df.count()}")

summary_df = cleaned_df \
        .groupBy("ProductID", "ProductName") \
        .agg(
            spark_sum("TotalSale").alias("TotalRevenue"),
            count("TransactionID").alias("NumberOfTransactions")
        ) \
        .orderBy(desc("TotalRevenue"))

print("Sales summary:")
summary_df.show()

print("Top 5 selling products:")
summary_df.limit(5).show()

output_path = os.path.join(output_dir, "product_sale_summary")
summary_df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(output_path)

print("Wrote summary")

spark.stop()
