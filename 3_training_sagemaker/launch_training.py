import sagemaker
from sagemaker.huggingface import HuggingFace
import os

def launch_training_job(
    role,
    train_data_path,
    validation_data_path,
    output_path,
    instance_type="ml.p3.2xlarge",
    model_name="t5-small",
    max_length=128,
    batch_size=8,
    learning_rate=5e-5,
    num_epochs=3
):
    # Initialize SageMaker session
    session = sagemaker.Session()
    
    # Define hyperparameters
    hyperparameters = {
        "model_name": model_name,
        "max_length": max_length,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "num_train_epochs": num_epochs
    }
    
    # Create HuggingFace estimator
    huggingface_estimator = HuggingFace(
        entry_point="train.py",
        source_dir=".",
        instance_type=instance_type,
        instance_count=1,
        role=role,
        transformers_version="4.26.0",
        pytorch_version="1.13.1",
        py_version="py39",
        hyperparameters=hyperparameters,
        output_path=output_path
    )
    
    # Define data channels
    data_channels = {
        "train": train_data_path,
        "validation": validation_data_path
    }
    
    # Start training
    huggingface_estimator.fit(data_channels)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", type=str, required=True, help="SageMaker execution role ARN")
    parser.add_argument("--train-data", type=str, required=True, help="S3 path to training data")
    parser.add_argument("--validation-data", type=str, required=True, help="S3 path to validation data")
    parser.add_argument("--output-path", type=str, required=True, help="S3 path for model output")
    parser.add_argument("--instance-type", type=str, default="ml.p3.2xlarge", help="SageMaker instance type")
    parser.add_argument("--model-name", type=str, default="t5-small", help="T5 model variant to use")
    
    args = parser.parse_args()
    
    launch_training_job(
        role=args.role,
        train_data_path=args.train_data,
        validation_data_path=args.validation_data,
        output_path=args.output_path,
        instance_type=args.instance_type,
        model_name=args.model_name
    ) 