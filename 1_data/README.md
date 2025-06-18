# Data Preparation

This directory contains scripts for preparing the mutated text dataset from the Project Gutenberg corpus using PySpark.

Specifically, we split the text into sentences of up to $n$ words (we'll use $n=20$ for simplicity), then create a user defined function (udf) in PySpark to mutate each sentence. Using a udf gives us the option of distributing the mutation over a several nodes.

We will store the data as follows:
```
mutated_data/
├── train/
│   ├── original.txt
│   └── mutated.txt
├── val/
│   ├── original.txt
│   └── mutated.txt
└── test/
    ├── original.txt
    └── mutated.txt
```
The data will be saved raw text with one line per sentence.

## Steps to Generate Dataset

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download a random sample of 100 books from Project Gutenberg:
```bash
python download_gutenberg.py --num-books 100 --output-file gutenberg.txt
```

3. (Optional) Start tracking the raw data with `dvc`
```bash
dvc add gutenberg.txt
```

4. Create the mutated/original pairs with Spark, and save text files.
```bash
python generate_mutated_dataset.py --max-sentence-len 20
```

5. Update the dvc record with the new data
```bash
dvc add mutated_data
```

6. Add the dvc record to git
```bash
git add mutated_data.dvc
git commit -m "Add mutated dataset"
```