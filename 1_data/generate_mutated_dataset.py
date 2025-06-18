import os
import argparse
from typing import List, Tuple
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StringType, ArrayType
from mutate_text import mutate_text
from download_gutenberg import download_subset_of_gutenberg_books

def split_into_sentences(text: str, max_words: int) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words) if words[i:i+max_words]]

def generate_dataset(input_dir: str, output_dir: str, mutation_rate: float = 0.05, max_sentence_len: int = 20):
    """Process Gutenberg books and create training pairs."""
    spark = SparkSession.builder \
        .appName("Text Mutation Generator") \
        .getOrCreate()
    
    # Create output directories
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)
    
    # Read all text files from the input directory
    df = spark.read.text(input_dir + "/*.txt")
    
    # UDF to split lines into sentences of up to max_sentence_len words
    split_udf = udf(lambda x: split_into_sentences(x, max_sentence_len), ArrayType(StringType()))
    df = df.withColumn("sentences", split_udf("value"))
    df = df.select(explode("sentences").alias("sentence"))
    
    # Register the mutation function as a UDF
    mutate_udf = udf(lambda x: mutate_text(x, mutation_rate), StringType())
    
    # Apply mutations and create training pairs
    df_mutated = df.withColumn("mutated_text", mutate_udf("sentence"))
    
    # Convert to pandas for easier text file writing
    pdf = df_mutated.select("sentence", "mutated_text").toPandas()
    
    # Split into train/val/test sets (80/10/10 split)
    train_size = int(len(pdf) * 0.8)
    val_size = int(len(pdf) * 0.1)
    
    train_df = pdf[:train_size]
    val_df = pdf[train_size:train_size + val_size]
    test_df = pdf[train_size + val_size:]
    
    # Write files for each split
    splits = {
        "train": train_df,
        "val": val_df,
        "test": test_df
    }
    
    for split_name, split_df in splits.items():
        # Write original texts
        original_file = os.path.join(output_dir, split_name, "original.txt")
        with open(original_file, "w", encoding="utf-8") as f:
            for text in split_df["sentence"]:
                f.write(f"{text}\n")
        
        # Write mutated texts
        mutated_file = os.path.join(output_dir, split_name, "mutated.txt")
        with open(mutated_file, "w", encoding="utf-8") as f:
            for text in split_df["mutated_text"]:
                f.write(f"{text}\n")
    
    print(f"Processed {len(pdf)} text pairs")
    print(f"Training pairs: {len(train_df)}")
    print(f"Validation pairs: {len(val_df)}")
    print(f"Test pairs: {len(test_df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mutated text dataset from Gutenberg corpus")
    parser.add_argument("--input-dir", default="gutenberg_books", help="Directory containing Gutenberg books")
    parser.add_argument("--output-dir", default="mutated_data", help="Output directory for training data")
    parser.add_argument("--mutation-rate", type=float, default=0.05, help="Probability of mutation per word")
    parser.add_argument("--num-books", type=int, default=10, help="Number of Gutenberg books to download")
    parser.add_argument("--max-sentence-len", type=int, default=20, help="Maximum number of words per sentence")
    
    args = parser.parse_args()
    
    # Download books if input directory is empty
    if not os.path.exists(args.input_dir) or not os.listdir(args.input_dir):
        print(f"Downloading {args.num_books} Gutenberg books...")
        download_subset_of_gutenberg_books(num_books=args.num_books)
    
    generate_dataset(args.input_dir, args.output_dir, args.mutation_rate, args.max_sentence_len) 