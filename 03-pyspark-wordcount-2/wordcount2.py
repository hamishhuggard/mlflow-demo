from pyspark.sql import SparkSession
import os

spark = SparkSession.builder \
        .appName("LoremIpsumWordcount") \
        .getOrCreate()

lorem_ipsum_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.

Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius,
turpis et dapibus dictum, nisi magna interdum elit, et lacinia erat risus sed
magna. Fusce ante ipsum, ultrices et a, sagittis quis, interdum vitae, libero.
Nunc et neque. Phasellus blandit leo ut odio. Maecenas felis tellus, dictum
eu, posuere ac, mattis sed, nulla. Aliquam eget lacus. Quisque sapien ut nunc
facilisis gravida. Ut id aliquet dui, in dictum lacus. Nulla facilisi.
Pellentesque at erat in est pellentesque dictum. Ut in ipsum.

Vivamus volutpat eros pulvinar velit. Proin facilisis arcu a elit. Nulla
facilisis, arcu at mollis aliquam, magna ligula sagittis est, at hendrerit
quam magna eu augue. Maecenas quis massa. Proin at elit non ante sollicitudin
facilisis. Praesent a sem in purus mollis adipiscing. Quisque eu mi a eros
molestie egestas. Maecenas ut est sed ante feugiat dictum. Nunc et erat.
Nullam non wisi a sem semper eleifend. Quisque ac lectus. Sed tempor.
Aliquam nonummy dictum enim. Donec volutpat enim quis odio.
"""

file_name = "lorem_ipsum_sample.txt"
try:
    with open(file_name, "w") as f:
        f.write(lorem_ipsum_text)
except IOError as e:
    print(f"Error creating {file_name}: {e}")
    spark.stop()
    exit()

lines = spark.sparkContext.textFile(file_name)
word_counts = lines.flatMap(lambda line: line.lower().split(" ")) \
        .filter(lambda word: word != "") \
        .map(lambda word: (word.strip().replace('.','').replace(',',''),1)) \
        .reduceByKey(lambda a, b: a+b)

sorted_word_counts = sorted(word_counts.collect(), key=lambda x: x[1], reverse=True)

for word, count in sorted_word_counts:
    print(f"{word}: {count}")

spark.stop()
