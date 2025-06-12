# T5 Text Mutation Training

This directory contains code for training a T5 model to perform text mutation using Amazon SageMaker.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Upload your data to S3:
```bash
aws s3 cp ../1_data/mutated_data/train/original.txt s3://your-bucket/data/train/original.txt
aws s3 cp ../1_data/mutated_data/train/mutated.txt s3://your-bucket/data/train/mutated.txt
aws s3 cp ../1_data/mutated_data/val/original.txt s3://your-bucket/data/val/original.txt
aws s3 cp ../1_data/mutated_data/val/mutated.txt s3://your-bucket/data/val/mutated.txt
```

## Training

Launch the training job using:

```bash
python launch_training.py \
    --role arn:aws:iam::<account-id>:role/service-role/AmazonSageMaker-ExecutionRole \
    --train-data s3://your-bucket/data/train \
    --validation-data s3://your-bucket/data/val \
    --output-path s3://your-bucket/models \
    --instance-type ml.p3.2xlarge \
    --model-name t5-small
```

### Parameters

- `--role`: SageMaker execution role ARN
- `--train-data`: S3 path to training data
- `--validation-data`: S3 path to validation data
- `--output-path`: S3 path for model output
- `--instance-type`: SageMaker instance type (default: ml.p3.2xlarge)
- `--model-name`: T5 model variant to use (default: t5-small)

## Model Architecture

The training script uses the Hugging Face Transformers library to fine-tune a T5 model. The model is trained to translate between original and mutated text pairs.

Key features:
- Uses T5's encoder-decoder architecture
- Implements sequence-to-sequence training
- Supports mixed precision training (FP16)
- Includes evaluation during training
- Saves checkpoints and final model

## Output

The trained model will be saved to the specified S3 output path. The model artifacts include:
- Model weights
- Tokenizer configuration
- Training configuration
- Evaluation metrics 