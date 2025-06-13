# Machine Learning and Data Portfolio

This is an demo project to prove competence with modern machine learning / data tools, including:
- Data:
    - Spark
    - dvc
- Training:
    - pytorch
    - mlflow
    - AWS Sagemaker
    - Azure ML
    - Huggingface
- Deployment:
    - FastAPI
    - Docker
    - Kubernetes
    - Azure ML
    - AWS sagemaker
- AI Agent and RAG
    - Langchain
- Batch inference
    - AWS Batch
    - Azure Batch
    - Snowflake
- Data streaming
    - AWS Kinesis, and Kinesis Analytics
    - Azure Event Hubs, Azure Stream Analytics
    - kinesis Data Analytics
- DevOps
    - Using Git actions

## Scenario

In the year 2030, Cloud providers introduce "DNA storage", in which they can cheaply store petabytes of data by encoding it in DNA.

But there's a problem: DNA is prone to the following [mutations](https://en.wikipedia.org/wiki/Mutation#Classification_of_types):
- *Deletions:* `hello` becomes `heo`
- *Duplications:* `hello` becomes `helello`
- *Inversion:* `hello` becomes `hlleo`
- *Insertions:* `hello` becomes `hel%kslo`
- *Substitutions:* `hello` becomes `hedfs`
- *Translocation:* `hello` becomes `lohel`

These corruptions would be very difficult to correct with traditional algorithms. But large language models (LLMs) can take into account context, the relative likely of differnet words and phrases, and pick out subtle patterns. We will therefore finetune an LLM to restore text that has been subjected to mutations.

We'll want to deploy the model in two ways:
1. As an API so that urgent mutation corrections can be queried immediately.
2. As a data stream, which will be collected and batch-processed once a day for non-urgent queries. 


### Dataset

We will use the [Project Gutenberg Corpus](https://arxiv.org/abs/1812.08092), which contains 3×10^9 tokens of clean and diverse text. To keep things simple, we'll perform the mutations on the level of characters rather than bytes.

### Model

Because this is a demo project, to keep costs low we'll use the smallest base model that has a decent shot of success. We will therefore use the small version of T5 (Text-to-Text Transfer Transformer), which is designed for text-to-text tasks, and only has 60M parameters. We'll reduce `max_seq_length` and `batch_size` drastically to keep costs low.

## Steps
1. Data preparation
- We will use **Spark** to generate the corrupted dataset, and **dvc** to version control the data.
2. Training the model
- We'll use **pytorch** to fine tune the model.
- We'll do some experiments locally **mlflow** for hyperparameter tuning.
- Once we've found some good hyperparameters, we'll do the actual training with **AWS Sagemaker**
3. Deploying the model API
- We can deploy the model directly with **AWS Sagemaker**
- We'll create an API with **FastPI** and put it in a **Docker** container.
- We'll then create a **Kubernetes** cluster to create an API service that self-heals and can scale with demand.
5. Data streaming
- We'll use **Amazon Kinesis Data Streams** for real-time data ingestion
- once a day, we'll trigger a lamdba function to write the data stream as json lines to s3 - We'll then use AWS glue to extract out just the text content, and write as .txt to s3 
- We'll then use sagemaker batch transform to transform the data to a corrected .txt file in s3 (or AWS batch?)
6. DevOps
- We'll also handle testing, type checking, and linting using **Github Actions**.


Alternatively, we could use Azure with Azure ML (training), Azure batch (batch processing), Azure Events Hugs (streams). That's left as a reader exercise.