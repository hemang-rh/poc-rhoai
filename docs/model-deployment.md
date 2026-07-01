# **OpenShift AI: Model Deployment Guide**

**1. Overview of Model Serving Platforms** OpenShift AI provides a robust environment to deploy trained machine-learning models to serve intelligent applications in production. For deploying large models, such as large language models (LLMs) or generative AI, the **single-model serving platform** (based on KServe) is recommended. This platform deploys each model on its own dedicated model server, helping teams efficiently monitor, scale, and maintain models that require significant compute resources.

_(Note: The legacy multi-model serving platform based on ModelMesh is deprecated in OpenShift AI 3.0, and migrating to the single-model serving platform is recommended.)_

**2. Flexible KServe Deployment Modes** The single-model serving platform offers two distinct deployment modes to suit your operational and infrastructure requirements:

- **Knative Serverless:** The default mode, which integrates with Red Hat OpenShift Serverless and OpenShift Service Mesh. It provides powerful autoscaling capabilities, including scaling up automatically based on request volume and scaling down to zero when idle to save costs.
- **KServe RawDeployment:** A traditional deployment method with fewer dependencies that does not require OpenShift Serverless. While it does not support scaling to zero by default, it is ideal for custom serving setups or models that must remain permanently active.

**3. Model Storage and "Modelcars" (OCI Containers)** OpenShift AI offers highly flexible options for where your model files reside prior to deployment. You can serve models directly from an **S3-compatible object storage** bucket, a **URI**, or a **Persistent Volume Claim (PVC)**. Additionally, you can use **Open Container Initiative (OCI) containers** (also known as _modelcars_ in KServe) for model storage. Packaging models as OCI images reduces startup times by avoiding repeated downloads, minimizes local disk space usage, and improves overall performance through pre-fetched images.

**4. Advanced LLM Serving and Distributed Inference** For enterprise-scale generative AI, OpenShift AI includes advanced capabilities for handling massive models:

- **Distributed Inference with llm-d:** A Kubernetes-native framework designed for serving LLMs at scale. It efficiently handles large models using optimizations like prefix-cache aware routing, disaggregated serving, and intelligent inference scheduling to maximize cache reuse and throughput.
- **Multi-Node GPU Deployment:** You can deploy extremely large models across multiple GPU nodes using the vLLM serving framework, which utilizes a specialized **`vllm-multinode-runtime`**.

**5. Secure, UI-Driven Deployment Workflow** Model deployment is highly streamlined via the "Deploy a model" wizard in the OpenShift AI dashboard.

- Administrators and data scientists can easily select the model source, assign a specific **Hardware Profile**, set CPU/Memory limits, and choose a **Serving Runtime** (such as the vLLM NVIDIA GPU runtime).
- To meet strict financial security requirements, deployments can be protected using **token authentication** tied to a specific Service Account.
- Models can be kept internal to the cluster or securely exposed to external clients by generating an external route.

---

**Relevant Official Documentation References**

You can refer your client to the following specific guides and chapters within the **Red Hat OpenShift AI Self-Managed 3.0** documentation suite for step-by-step implementation:

- **For Platform Architecture and Setup:**
  - _Document:_ [**About model-serving platforms**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/configuring_your_model-serving_platform/configuring-your-model-serving-platform_rhoai-admin) and [**Configuring model servers on the single-model serving platform**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/configuring_your_model-serving_platform/configuring_model_servers)
    - _Details:_ Explains the differences between serving platforms, available runtimes, KServe deployment modes, and how to enable speculative decoding and multi-modal inferencing.
- **For UI-Driven Model Deployment:**
  - _Document:_ [**Deploying models on the single-model serving platform**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/deploying_models/deploying_models)
    - _Details:_ Provides the step-by-step UI wizard instructions for deploying a model, attaching hardware profiles, setting compute limits, and enforcing token authentication.
- **For Model Storage and OCI Images:**
  - _Document:_ [**Storing models**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/deploying_models/deploying-models_rhoai-user)
    - _Details:_ Covers how to upload model files to a PVC, as well as how to build and deploy models stored in OCI containers (modelcars).
- **For Advanced LLM Scaling:**
  - _Document:_ [**Managing and monitoring models**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_and_monitoring_models/managing_and_monitoring_models)
    - _Details:_ Details how to configure multi-node GPU deployments with vLLM, estimate memory needs for LLM-powered applications, and utilize quantization to reduce memory footprints
