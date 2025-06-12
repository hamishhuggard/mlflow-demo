import os
import argparse
import torch
from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import load_dataset
import numpy as np
from typing import Dict, List, Union

def parse_args():
    parser = argparse.ArgumentParser()
    
    # Data and model parameters
    parser.add_argument("--train_file", type=str, required=True)
    parser.add_argument("--validation_file", type=str, required=True)
    parser.add_argument("--model_name", type=str, default="t5-small")
    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--output_dir", type=str, default="/opt/ml/model")
    
    return parser.parse_args()

def prepare_dataset(tokenizer, file_path: str, max_length: int):
    """Load and prepare dataset from text files."""
    dataset = load_dataset('text', data_files={'train': file_path})
    
    def preprocess_function(examples):
        # Split into original and mutated pairs
        pairs = [line.split('\t') for line in examples['text']]
        original_texts = [pair[0] for pair in pairs]
        mutated_texts = [pair[1] for pair in pairs]
        
        # Tokenize inputs and targets
        model_inputs = tokenizer(
            original_texts,
            max_length=max_length,
            truncation=True,
            padding="max_length"
        )
        
        labels = tokenizer(
            mutated_texts,
            max_length=max_length,
            truncation=True,
            padding="max_length"
        )
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    return dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=dataset["train"].column_names
    )

def main():
    args = parse_args()
    
    # Initialize tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    
    # Prepare datasets
    train_dataset = prepare_dataset(tokenizer, args.train_file, args.max_length)["train"]
    eval_dataset = prepare_dataset(tokenizer, args.validation_file, args.max_length)["train"]
    
    # Training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="epoch",
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.num_train_epochs,
        weight_decay=0.01,
        save_total_limit=3,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),
    )
    
    # Initialize trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model)
    )
    
    # Train the model
    trainer.train()
    
    # Save the model
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

if __name__ == "__main__":
    main() 