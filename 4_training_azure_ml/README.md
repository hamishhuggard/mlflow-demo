# T5 Text Mutation Training on Azure ML

This directory contains code for training a T5 model to perform text mutation using Azure Machine Learning.

## Setup

1. Install the Azure ML SDK:
```bash
pip install azureml-core azureml-dataset-runtime azureml-defaults
```

2. Configure Azure credentials:
```bash
az login
```

3. Create an Azure ML workspace (if you don't have one):
```bash
az ml workspace create --name <workspace-name> --resource-group <resource-group>
```

4. Upload your data to Azure ML:
```bash
az ml data create --name train-data --path ../1_data/mutated_data/train
az ml data create --name val-data --path ../1_data/mutated_data/val
```

## Training

Launch the training job using:

```bash
python launch_training.py \
    --subscription-id <subscription-id> \
    --resource-group <resource-group> \
    --workspace-name <workspace-name> \
    --compute-name <compute-name> \
    --train-data <train-data-path> \
    --validation-data <validation-data-path> \
    --model-name t5-small \
    --vm-size STANDARD_NC6
```

### Parameters

- `--subscription-id`: Azure subscription ID
- `--resource-group`: Azure resource group name
- `--workspace-name`: Azure ML workspace name
- `--compute-name`: Name for the compute target
- `--train-data`: Path to training data
- `--validation-data`: Path to validation data
- `--model-name`: T5 model variant to use (default: t5-small)
- `--vm-size`: Azure VM size (default: STANDARD_NC6)

## Model Architecture

The training script uses the Hugging Face Transformers library to fine-tune a T5 model. The model is trained to translate between original and mutated text pairs.

Key features:
- Uses T5's encoder-decoder architecture
- Implements sequence-to-sequence training
- Supports mixed precision training (FP16)
- Includes evaluation during training
- Saves checkpoints and final model
- Integrates with Azure ML's experiment tracking
- Uses TensorBoard for visualization

## Output

The trained model will be:
1. Saved to the specified output directory
2. Registered in Azure ML's model registry
3. Available for deployment through Azure ML

The training run will be tracked in Azure ML's experiment tracking system, where you can:
- Monitor training progress
- View metrics and logs
- Compare different runs
- Access TensorBoard visualizations

## Monitoring

You can monitor the training job through:
1. Azure ML Studio UI
2. TensorBoard integration
3. Azure ML SDK
4. Azure Portal

The training metrics and logs will be automatically tracked and can be viewed in the Azure ML Studio. 