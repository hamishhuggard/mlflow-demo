import kubernetes.client
import kubernetes.config
import yaml
import os

def deploy_to_eks(manifest_path, namespace="default"):
    kubernetes.config.load_kubernetes_config() # load kubectl context for EKS

    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)

    api_client = kubernetes.client.ApiClient()

    try:
        if manifest['Kind'] == 'Deployment':
            api_instance = kubernetes.client.AppsV1Api(api_client)
            api_instance.create_namespace_deployment(body=manifest, namespace=namespace)
            print(f"Deployment {manifest['metadata']['name']} created successfully")
        elif manifest['Kind'] == 'Service':
            api_instance = kubernetes.client.AppsV1Api(api_client)
            api_instance.create_namespace_service(body=manifest, namespace=namespace)
            print(f"Service {manifest['metadata']['name']} created successfully")
        else:
            print("Only deployments and services are supported by this script")
    except Kubernetes.ApiException as e:
        print(f"Error deploying {manifest_path}: {e}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_dir = os.path.join(current_dir, "k8s_manifests"))
    deployment_yaml = os.path.join(manifest_dir, "deployment.yaml")
    service_yaml = os.path.join(manifest_dir, "service.yaml")
    deploy_to_eks(deployment_yaml)
    deploy_to_eks(service_yaml)



