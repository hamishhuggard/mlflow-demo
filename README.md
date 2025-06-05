# Notes on ML Engineering

This is an demo project to prove competence with modern machine learning / data tools.

The project idea is simple: we will introduce errors into a corpus of text, and finetune an LLM to restore the original text.

Our text corruption will be inspired by how DNA is corrupted:
- *Deletions:* `hello world` becomes `hellorld`
- *Substitutions:* `hello world` becomes `h3jso world`
- *Insertions:* `hello world` becomes `hello wos8%srld`
- *Duplications:* `hello world` becomes `hello world`
- *Reversals:* `hello world` becomes `hello world`
These corruptions would be very difficult to correct with traditional algorithms, but hopefully an LLM can achieve reasonable accuracy using context cues and learning subtle patterns.

1. Data preparation
2. Training the model
3. Deploying the model
4. Batch inference
4. Data stream

1. Data management
- [01_data](01_data) We will use `PySpark` to generate the dataset and `dvc` to 
- [02_dvc](01_dvc) PySpark

## Skills to learn

[According to Gemini](https://gemini.google.com/app/a8233c77cee25212?hl=en_GB), here's how I should prioritise my learning:

### Top priority:
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
  - Spark is the industry standard for large-scale data manipulation and often integrates with ML frameworks (MLlib) and platforms like Databricks.
  - Difficulty: Medium to High. Concepts like distributed computing and lazy evaluation can be tricky, but it's incredibly powerful.

### High Priority (Significant Impact, Build on Existing Strengths):
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

### Medium Priority (Valuable Additions, Address Specific Gaps):
- Data Lake and Data Warehouse Concepts (including ETL/ELT):
    - Focus: Understand the fundamental differences between data lakes and data warehouses (schema-on-read vs. schema-on-write, data types, use cases). Grasp the concepts of ETL (Extract, Transform, Load) and E
- LT (Extract, Load, Transform) pipelines and when to use each.
    - Why it's important: As an ML Engineer, you're the bridge between data and models. Understanding where your data comes from and how it's prepared is crucial for building robust ML pipelines and debugging data-related issues.
    - Difficulty: Easy to Medium. It's more conceptual understanding than tool mastery, but practical examples are helpful.
- DVC (Data Version Control) - Deeper Dive:
    - Focus: Go beyond basic CLI commands. Understand how DVC integrates with Git, handles large files, and enables pipeline reproducibility. Explore DVC "pipelines" for orchestrating ML workflows.
    - Why it's important: Reproducibility of experiments and data lineage are critical in MLOps. Your basic understanding is a great start.
    - Difficulty: Easy. DVC is conceptually straightforward once you grasp its core purpose. A few days of dedicated practice will solidify your understanding.

### Lower Priority (Good to Know, but Not Always Core ML Engineering):
- Weights & Biases (W&B) or Neptune.ai (Choose one to focus on):
    - Focus: Get proficient with one of these for experiment tracking and visualization. While MLflow is strong, W&B and Neptune offer more advanced visualization capabilities and collaborative features.
    - Why it's important: It shows flexibility and experience with various experiment tracking paradigms. It's a valuable skill for collaboration with data scientists.
    - Difficulty: Easy. They are generally user-friendly.
- PowerBI or Tableau (Choose one, if interested in visualization/reporting):
    - Focus: As an ML Engineer, your primary role isn't usually creating dashboards, but being able to connect to data sources (e.g., model logs, prediction outputs) and create basic visualizations of model performance or business impact can be a valuable soft skill.
    - Why it's important: While not core ML engineering, it aids in communicating results and monitoring. PowerBI might be slightly more prevalent in corporate environments that lean heavily into Microsoft.
    - Difficulty: Easy to Medium. Becoming proficient enough for ML-related dashboards will take some dedicated practice.


## Cloud techs to learn

| Technology Category | AWS Specifics (Examples) | Azure Specifics (Examples) | Learning Priority | Notes |
| :------------------ | :----------------------- | :--------------------------- | :---------------- | :---- |
| **ML Platform Services** | **SageMaker:** Studio, Training Jobs, Endpoints (Real-time, Batch), Model Registry, Pipelines, Clarify/Monitor. | **Azure Machine Learning:** Workspace, Compute (Instances/Clusters), Jobs (Training/Batch), Endpoints, Model Registry, Pipelines, Responsible AI Dashboard/Monitor. | **Highest** | This is the core for ML Engineers. Aim for deep proficiency in one, and a strong conceptual understanding of the other. These services cover the entire ML lifecycle. |
| **Container Orchestration** | **EKS (Elastic Kubernetes Service):** Deploying applications, scaling, basic `kubectl` commands, networking (Load Balancers/Ingress). | **AKS (Azure Kubernetes Service):** Deploying applications, scaling, basic `kubectl` commands, networking (Load Balancers/Ingress). | **High** | Even if ML Platforms abstract K8s, understanding the underlying concepts and how to deploy your own services (like FastAPI) is crucial. |
| **Cloud Storage** | **S3 (Simple Storage Service):** Buckets, objects, access control, versioning, lifecycle policies, S3 Glacier for archiving. | **Azure Blob Storage / Data Lake Storage Gen2:** Containers, blobs, access tiers, lifecycle management. | **High** | Fundamental for storing data, model artifacts, and logs. Essential for any ML pipeline. |
| **Identity & Access Management** | **IAM (Identity and Access Management):** Users, Roles, Policies, Service Roles for ML services. | **Azure Active Directory (Azure AD):** Service Principals, Managed Identities, Roles, Role-Based Access Control (RBAC). | **High** | Crucial for securing your ML resources and pipelines. Understand least privilege. |
| **Distributed Data Processing** | **EMR (Elastic MapReduce) with PySpark:** Running Spark jobs on managed clusters. | **Azure Databricks (built on Spark) / Azure Synapse Analytics (Spark Pools):** Running Spark workloads. | **High** | For handling large datasets, essential for feature engineering and large-scale model training. |
| **Data Warehousing & Lakes** | **Redshift:** Managed data warehouse. **Glue:** ETL, Data Catalog. **Athena:** Serverless query for S3 data. **Lake Formation:** Data lake governance. | **Azure Synapse Analytics:** Unified analytics, data warehousing. **Azure Data Factory:** ETL/ELT orchestration. **Azure Data Lake Storage Gen2:** Scalable data lake. | **Medium** | Understanding data flow from raw to features is vital. Focus on the concepts and how these services facilitate them. |
| **Infrastructure as Code (IaC)** | **Terraform (preferred for multi-cloud) / CloudFormation (AWS-specific).** | **Terraform (preferred for multi-cloud) / ARM Templates (Azure-specific).** | **Medium** | For reproducible and version-controlled infrastructure deployments, highly valued in production environments. |
| **Serverless Compute** | **Lambda:** Event-driven functions, integrating with S3/API Gateway for simple ML tasks. | **Azure Functions:** Event-driven functions, integrating with Blob Storage/API Management. | **Medium** | Useful for lightweight automation, event triggers in MLOps pipelines, or simple inference endpoints. |
| **Monitoring & Logging** | **CloudWatch:** Logs, metrics, alarms for EC2, Lambda, SageMaker. | **Azure Monitor:** Logs, metrics, alerts for Azure ML, AKS, Azure Functions. | **Medium** | Essential for observing the health and performance of your ML systems post-deployment. |

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

## Kubernetes 

### Concepts:

- Pod ~= a wrapper for a (non-self healing) container
  - or multiple containers that share a storage and localhost
- ReplicaSet: makes sure there are n identical pods running at all times
- Deployment: a set of ReplicaSets
  - eg, {v1, v2}
  - v2 can be spun while v1 is spun down for zero downtime.
- the pods exist within a virtual network within the cluster, and each has its own IP address
  - in kind (k8s in docker), the cluster is inside a container
  - in docker desktop, the cluster is inside a VM
- Service provides a single IP address to all the pods in a Deployment/Replicaset/Pod
  - ClusterIP does a basic load balancing within the cluster
  - NodePort also gives the service a port to talk to the outside world
  - LoadBalancer uses the cloud's load balancer to distribute traffice outside the cluster
  - The Service operates on the TCP/IP level
- Ingress exposes the cluster to the outside world via the HTTP/s layer
  - host-based routing (api.app.com vs test.app.com)
  - path-based routing (app.com/api vs app.com/test)
  - SSL termination
- StatefulSet ~= Deployment with shared storage (good for DB)
- Job: creates one or more pods and ensures a sufficient number terminate
- CronJob: job but it runs on a schedule

### Kubectl commands
Get a list of live pods:
```
kubectl get pods
```
Get a list of live deployments
```
kubectl get deployments
```
Etc:
```
kubectl get services
kubectl get ingress
kubectl get all
```

```
kubectl describe pod pod-1
kubectl describe deployement deployment-1
kubectl describe service service-1
```

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

## EKS and AKS

- Programatic development in Python involves two levels:
  - Cloud SDK (boto3 or Azure SDK) for managing the _cluster_
  - K8s python client (for managing resources _within_ the cluster, like pods, services, etc)
- Azure:
    - `azure-mgmt-containerservice` library
    - `managed_cluster.create_or_update` to create or update a cluster
    - `managed_cluster.get` 
    - `managed_cluster.delete` 
    - `managed_cluster.list_by_resource_group` to list clusters
    - `managed_cluster.list_cluster_user_credentials` or `managed_cluster.list_cluster_admin_credentials` to obtain the `kubeconfig` for connecting to the clusters k8s API

## Joblib

joblib is recommended over pickle for storing/loading with ml libraries because it's more efficient with NumPy arrays. 

## Async functions

The following has some slight inaccuracies in the language when i talk about the event loop, but I think conceptually it's sound

- async functions give us i/o concurrency, but not multithreading
- an async function can call sync functions (normal functions) or async functions
- but a sync function cannot call async functions
    - except via async.run(async_function)
- await async_function() means "run async_function, and pause this coroutine until the async_function is done"
- await async.gather(async_1(), async_2(), async_3()) means "run the async functions together, and pause this coroutine until they're all done"
- under the hood what's actually happening is:
- calling an async function creates a Coroutine object
- await coroutine_1 means "add coroutine_1 to the event loop, block the currrent coroutine, and hand control over to the event loop to start running the next non-blocked coroutine"
- async.create_task(coroutine_1) means "add coroutine_1 to the event loop and return a Task object")
- await task_1 is the same as await coroutine_1
- async.gather adds all the coroutines to the event loop then blocks the currenet coroutine
