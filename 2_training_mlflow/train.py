import os
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration, AdamW
import mlflow
import mlflow.pytorch
from typing import Dict, Any, List, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
import json
import random
from pathlib import Path

class MutationDataset(Dataset):
    def __init__(self, texts: list, targets: list, tokenizer: T5Tokenizer, max_length: int = 512):
        self.texts = texts
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        target = self.targets[idx]

        # Prepare the input text
        input_text = f"restore text: {text}"
        
        # Tokenize inputs and targets
        inputs = self.tokenizer(input_text, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")
        targets = self.tokenizer(target, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze()
        }

def generate_random_hyperparameters() -> Dict[str, Any]:
    """Generate random hyperparameters for training."""
    return {
        "model_name": random.choice(["t5-small", "t5-base"]),
        "batch_size": random.choice([4, 8, 16, 32]),
        "learning_rate": random.uniform(1e-5, 1e-3),
        "num_epochs": random.randint(2, 5),
        "max_length": random.choice([256, 512, 768]),
        "weight_decay": random.uniform(0.0, 0.1),
        "warmup_steps": random.randint(0, 1000),
        "gradient_accumulation_steps": random.choice([1, 2, 4])
    }

def train_model(
    train_data: pd.DataFrame,
    val_data: pd.DataFrame,
    model_name: str = "t5-small",
    batch_size: int = 8,
    learning_rate: float = 1e-4,
    num_epochs: int = 3,
    max_length: int = 512,
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
) -> Tuple[Dict[str, Any], float]:
    
    # Initialize tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)

    # Create datasets
    train_dataset = MutationDataset(
        train_data["mutated_text"].tolist(),
        train_data["original_text"].tolist(),
        tokenizer,
        max_length
    )
    val_dataset = MutationDataset(
        val_data["mutated_text"].tolist(),
        val_data["original_text"].tolist(),
        tokenizer,
        max_length
    )

    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    # Initialize optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    # Start MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params({
            "model_name": model_name,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "num_epochs": num_epochs,
            "max_length": max_length
        })

        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            # Training
            model.train()
            total_train_loss = 0
            optimizer.zero_grad()
            
            for i, batch in enumerate(train_loader):
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )

                loss = outputs.loss
                total_train_loss += loss.item()

                loss.backward()

                if (i + 1) % gradient_accumulation_steps == 0:
                    optimizer.step()
                    optimizer.zero_grad()

            avg_train_loss = total_train_loss / len(train_loader)
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)

            # Validation
            model.eval()
            total_val_loss = 0
            
            with torch.no_grad():
                for batch in val_loader:
                    input_ids = batch["input_ids"].to(device)
                    attention_mask = batch["attention_mask"].to(device)
                    labels = batch["labels"].to(device)

                    outputs = model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=labels
                    )

                    total_val_loss += outputs.loss.item()

            avg_val_loss = total_val_loss / len(val_loader)
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)

            # Save best model
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                mlflow.pytorch.log_model(model, "model")

            print(f"Epoch {epoch + 1}/{num_epochs}")
            print(f"Average training loss: {avg_train_loss:.4f}")
            print(f"Average validation loss: {avg_val_loss:.4f}")

        return {
            "model": model,
            "tokenizer": tokenizer,
            "best_val_loss": best_val_loss
        }, best_val_loss

def save_best_hyperparameters(hyperparameters: Dict[str, Any], val_loss: float):
    """Save the best hyperparameters to a JSON file."""
    output_dir = Path("../best_hyperparameters")
    output_dir.mkdir(exist_ok=True)
    
    output = {
        "hyperparameters": hyperparameters,
        "validation_loss": val_loss,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    
    with open(output_dir / "best_hyperparameters.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train T5 model for text restoration")
    parser.add_argument("--data-path", required=True, help="Path to the parquet file containing the dataset")
    parser.add_argument("--num-trials", type=int, default=10, help="Number of hyperparameter search trials")
    
    args = parser.parse_args()
    
    # Load and split data
    df = pd.read_parquet(args.data_path)
    train_data, val_data = train_test_split(df, test_size=0.1, random_state=42)
    
    # Perform hyperparameter search
    best_val_loss = float('inf')
    best_hyperparameters = None
    
    for trial in range(args.num_trials):
        print(f"\nTrial {trial + 1}/{args.num_trials}")
        
        # Generate random hyperparameters
        hyperparameters = generate_random_hyperparameters()
        print("Hyperparameters:", hyperparameters)
        
        # Train model with current hyperparameters
        _, val_loss = train_model(
            train_data=train_data,
            val_data=val_data,
            **hyperparameters
        )
        
        # Update best hyperparameters if current trial is better
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_hyperparameters = hyperparameters
            print(f"New best validation loss: {best_val_loss:.4f}")
    
    # Save best hyperparameters
    save_best_hyperparameters(best_hyperparameters, best_val_loss)
    print("\nBest hyperparameters saved to ../best_hyperparameters/best_hyperparameters.json") 