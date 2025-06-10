# Data Preparation

This directory contains scripts for preparing the mutated text dataset from the Project Gutenberg corpus.

## Steps to Generate Dataset

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download a random sample of 100 books from Project Gutenberg:
```bash
python download_gutenberg.py --num-books 100 --output-file gutenberg.txt
```

3. Start tracking the raw data with `dvc`
```bash
dvc add gutenberg.txt
```

4. Create the mutated/original pairs with Spark, and save text files.
```bash
```

5. Update the dvc record
```bash
```

6. Add the dvc record to git
```bash
```

```bash
dvc add mutated_data
git add mutated_data.dvc
git commit -m "Add mutated dataset"
``` 

## Output Format

Files are organized as:
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
The data is saved in text files with one line per sentence, truncated after 20 words.