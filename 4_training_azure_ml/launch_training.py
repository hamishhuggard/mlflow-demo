from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
import os

def get_or_create_compute(workspace, compute_name, vm_size="STANDARD_NC6"):
    """Get or create an Azure ML compute target."""
    try:
        compute_target = ComputeTarget(workspace=workspace, name=compute_name)
        print(f"Found existing compute target: {compute_name}")
    except ComputeTargetException:
        print(f"Creating new compute target: {compute_name}")
        compute_config = AmlCompute.provisioning_configuration(
            vm_size=vm_size,
            max_nodes=1
        )
        compute_target = ComputeTarget.create(
            workspace=workspace,
            name=compute_name,
            provisioning_configuration=compute_config
        )
        compute_target.wait_for_completion(show_output=True)
    
    return compute_target

def launch_training_job(
    subscription_id,
    resource_group,
    workspace_name,
    compute_name,
    train_data_path,
    validation_data_path,
    model_name="t5-small",
    max_length=128,
    batch_size=8,
    learning_rate=5e-5,
    num_epochs=3,
    vm_size="STANDARD_NC6"
):
    # Connect to workspace
    workspace = Workspace(
        subscription_id=subscription_id,
        resource_group=resource_group,
        workspace_name=workspace_name
    )
    
    # Get or create compute target
    compute_target = get_or_create_compute(workspace, compute_name, vm_size)
    
    # Create environment
    env = Environment.from_conda_specification(
        name="t5-training-env",
        file_path="environment.yml"
    )
    
    # Create script config
    script_config = ScriptRunConfig(
        source_directory=".",
        script="train.py",
        compute_target=compute_target,
        environment=env,
        arguments=[
            "--train_file", train_data_path,
            "--validation_file", validation_data_path,
            "--model_name", model_name,
            "--max_length", str(max_length),
            "--batch_size", str(batch_size),
            "--learning_rate", str(learning_rate),
            "--num_train_epochs", str(num_epochs)
        ]
    )
    
    # Create and submit experiment
    experiment = Experiment(workspace=workspace, name="t5-text-mutation")
    run = experiment.submit(script_config)
    
    # Print run details
    print(f"Submitted training run: {run.id}")
    print(f"Run URL: {run.get_portal_url()}")
    
    return run

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription-id", type=str, required=True)
    parser.add_argument("--resource-group", type=str, required=True)
    parser.add_argument("--workspace-name", type=str, required=True)
    parser.add_argument("--compute-name", type=str, required=True)
    parser.add_argument("--train-data", type=str, required=True)
    parser.add_argument("--validation-data", type=str, required=True)
    parser.add_argument("--model-name", type=str, default="t5-small")
    parser.add_argument("--vm-size", type=str, default="STANDARD_NC6")
    
    args = parser.parse_args()
    
    launch_training_job(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        compute_name=args.compute_name,
        train_data_path=args.train_data,
        validation_data_path=args.validation_data,
        model_name=args.model_name,
        vm_size=args.vm_size
    ) 