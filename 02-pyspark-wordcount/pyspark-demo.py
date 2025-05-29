from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower

spark = SparkSession.builder \
        .appName("SimpleWordCount") \
        .getOrCreate()

data = [
    ("This is the first sentence",),
    ("This is the second sentence",),
    ("Wow, would you believe that it's another sentence already?",)
]

schema = ["text"]
df = spark.createDataFrame(data, schema)

print("Original data frame:")
df.show(truncate=False)

words_df = df.select(explode(split(lower(df.text), " ")).alias("word"))

print("Dataframe after splitting into words:")
words_df.show()

filtered_words_df = words_df.filter(words_df.word != "")

print("Dataframe after filtering:")
filtered_words_df.show()

word_counts = filtered_words_df.groupBy("word").count()

print("Final word count:")
word_counts.show()

spark.stop()

