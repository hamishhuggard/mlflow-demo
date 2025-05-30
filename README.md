# Datascience Skills

According to Gemini, here's how I should prioritise my learning:

## Top priority:
  - Kubernetes (Deeper Conceptual Understanding & Practical Application):
    - Understand Pods, Deployments, Services, Ingress, and how they relate to deploying and scaling ML models. Learn about kubectl commands for managing resources.
    - Why it's important: While cloud providers offer managed services (like EKS, AKS), the underlying concepts of Kubernetes are crucial. Many MLOps tools (like Kubeflow, Seldon) are built on Kubernetes.
    - Difficulty: Medium to High
  - Cloud ML Services (AWS SageMaker / Azure Machine Learning)
    - AWS: Focus on SageMaker (Studio, Training Jobs, Endpoints for real-time inference, Batch Transform, Model Registry, Monitoring). Also understand how S3, ECR, and IAM integrate with SageMaker.
    - Azure: Focus on Azure Machine Learning workspace (Experiments, Training, Endpoints for real-time inference, Pipelines, Model Registry, Monitoring). Understand integration with Azure Blob Storage, Azure Container Registry (ACR), and Azure Active Directory.
    - Estimated Difficulty: Medium
  - Apache Spark (PySpark focus):
    - Understand Spark DataFrames, common transformations (joins, aggregations), and how to read/write from various data sources (CSV, Parquet, Delta Lake). Get familiar with SparkSession and the Spark ecosystem.
    -  Spark is the industry standard for large-scale data manipulation and often integrates with ML frameworks (MLlib) and platforms like Databricks.
    - Difficulty: Medium to High. Concepts like distributed computing and lazy evaluation can be tricky, but it's incredibly powerful.

## High Priority (Significant Impact, Build on Existing Strengths):
- MLflow: 
    - MLflow Model Registry: Managing model versions, stages (Staging, Production), and approval workflows.
    - MLflow Projects: Packaging code for reproducible runs.
    - MLflow Deployments: How to use MLflow to deploy models to various targets (e.g., local, Docker, Kubernetes, cloud platforms).
    - Why it's important: It's a widely adopted open-source MLOps tool, and deepening your existing knowledge will make you highly effective in environments that use it.
    - Estimated Difficulty: Easy to Medium (building on your existing foundation). A week or two of dedicated practice should get you proficient.
- Databricks (MLflow Integration, Notebooks, Jobs, Delta Lake):
    - Focus: Learn Databricks, specifically its integration with MLflow. Understand how to use Databricks notebooks for ML experimentation, schedule jobs for training pipelines, and leverage Delta Lake for reliable data storage within Databricks.
    - Why it's important: Databricks is very popular for large-scale data and ML, often seen alongside Spark and MLflow. Many companies in Auckland (and globally) use it.
    - Difficulty: Medium. Learning Spark first helps. Hands-on labs are key here.

## Medium Priority (Valuable Additions, Address Specific Gaps):
- Data Lake and Data Warehouse Concepts (including ETL/ELT):
    - Focus: Understand the fundamental differences between data lakes and data warehouses (schema-on-read vs. schema-on-write, data types, use cases). Grasp the concepts of ETL (Extract, Transform, Load) and E
- LT (Extract, Load, Transform) pipelines and when to use each.
    - Why it's important: As an ML Engineer, you're the bridge between data and models. Understanding where your data comes from and how it's prepared is crucial for building robust ML pipelines and debugging data-related issues.
    - Difficulty: Easy to Medium. It's more conceptual understanding than tool mastery, but practical examples are helpful.
- DVC (Data Version Control) - Deeper Dive:
    - Focus: Go beyond basic CLI commands. Understand how DVC integrates with Git, handles large files, and enables pipeline reproducibility. Explore DVC "pipelines" for orchestrating ML workflows.
    - Why it's important: Reproducibility of experiments and data lineage are critical in MLOps. Your basic understanding is a great start.
    - Difficulty: Easy. DVC is conceptually straightforward once you grasp its core purpose. A few days of dedicated practice will solidify your understanding.

## Lower Priority (Good to Know, but Not Always Core ML Engineering):
- Weights & Biases (W&B) or Neptune.ai (Choose one to focus on):
    - Focus: Get proficient with one of these for experiment tracking and visualization. While MLflow is strong, W&B and Neptune offer more advanced visualization capabilities and collaborative features.
    - Why it's important: It shows flexibility and experience with various experiment tracking paradigms. It's a valuable skill for collaboration with data scientists.
    - Difficulty: Easy. They are generally user-friendly.
- PowerBI or Tableau (Choose one, if interested in visualization/reporting):
    - Focus: As an ML Engineer, your primary role isn't usually creating dashboards, but being able to connect to data sources (e.g., model logs, prediction outputs) and create basic visualizations of model performance or business impact can be a valuable soft skill.
    - Why it's important: While not core ML engineering, it aids in communicating results and monitoring. PowerBI might be slightly more prevalent in corporate environments that lean heavily into Microsoft.
    - Difficulty: Easy to Medium. Becoming proficient enough for ML-related dashboards will take some dedicated practice.

## Project outline
Prioritize hands-on projects that integrate multiple tools from the higher priority tiers:
- Use Spark for data preprocessing.
- Train a model, tracking experiments with MLflow.
- Containerize the model with Docker.
- Deploy the model as an API (FastAPI) to a Kubernetes cluster (e.g., Minikube locally, then potentially EKS/AKS).
- Manage data/model versions with DVC.

## Data Lakes and Data Warehouses

| Concept              | Typical Access Interface       | Common Data Pipeline Approach | AWS Offering        | Azure Offering                      |
| :------------------- | :----------------------------- | :---------------------------- | :------------------ | :---------------------------------- |
| **Data Warehouse** | **SQL Queries** (via JDBC/ODBC) | **ETL** | **Amazon Redshift** | **Azure Synapse Analytics** (Dedicated SQL Pool) |
| **Data Lake** | **URIs** (for file access) / **SQL** (via query engines like Athena) | **ELT** | **Amazon S3** | **Azure Data Lake Storage Gen2 (ADLS Gen2)** |

ETL = Extract, transform, load, means transforming the data into the preferred format as it is injested into the data storage.
ELT = Extract, load, transform, means storing the raw data in the storage as-is, and transforming it into the desired format on reads.

Then there's a "Lakehouse" which does something like keep the raw data in blob storage but maintains a SQL server as an index on the data.

Spark is basically pandas for big data. It's distributed, fault tolerant, does lazy execution, and handles analytics and ML.
(Under the hood it's completely different to pandas. But the API is broadly simialr.)

## Docker concepts:
- node = a physical (or virtual) server
- pod ~= a set of containers for one node
- deployment = process that runs or kills containers to meet specs
- service ~= nginx. reverse proxy and load balancer.
- ingress ~= routing URLs to specific services and SSL certification

## Kubectl commands
```
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get all

kubectl describe pod pod-1
kubectl describe deployement deployment-1
kubectl describe service service-1

kubectl apply -f deployment.yaml

kubectl delete deployment deployment-1

kubectl logs pod-1

# run command inside of the pod's container
kubectl exec -it pod-1 -- <command> 
# get shell inside container
kubectl exec -it pod-1 -- bash 

# manually scale deployment to 5 replicas
kubectl scale deployment deployment-1 --replicas=5 

kubectl rollout status deployment/first-deployment
kubectl rollout history deployment/first-deployment
kubectl rollout undo deployment/first-deployment
```

## Azure and AWS kubernetes offerings
| Azure Offering             | AWS Offering                  |
| :------------------------- | :---------------------------- |
| **Azure Kubernetes Service (AKS)** | **AWS Elastic Kubernetes Service (EKS)** |
