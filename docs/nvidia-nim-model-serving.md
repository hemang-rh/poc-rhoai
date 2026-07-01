# **OpenShift AI: NVIDIA NIM Model Serving Guide**

**1. Overview of NVIDIA NIM on OpenShift AI** NVIDIA NIM is a set of microservices within NVIDIA AI Enterprise designed for the secure, reliable deployment of high-performance AI model inferencing across data centers and clouds. In OpenShift AI, the NVIDIA NIM model serving platform is built on top of the single-model serving platform (KServe). It provides highly optimized container inferencing for both open-source community models and NVIDIA AI Foundation models.

**2. Enabling the NVIDIA NIM Model Serving Platform** Before your teams can deploy NIM containers, the platform must be properly enabled by an administrator:

- **Prerequisites:** You must first install the single-model serving platform and enable GPU support on the cluster using the Node Feature Discovery and NVIDIA GPU Operators. You also must have an NVIDIA Cloud Account (NCA), access to the NVIDIA GPU Cloud (NGC) portal, and a personal API key.
- **Activation:** Administrators can activate NIM by navigating to **Applications → Explore** in the OpenShift AI dashboard, selecting the **NVIDIA NIM** tile, clicking **Enable**, and entering their personal NVIDIA API key.

**3. Running and Deploying NIM Models** Once enabled, deploying a NIM model is a streamlined process with customizable configurations:

- **Deployment Workflow:** Users can navigate to the **Deployments** tab within their project, select the **NVIDIA NIM** model serving platform tile, and click **Deploy model**.
- **Resource Configuration:** During deployment, users select their desired model from the NIM list and configure its properties, including the number of replicas, hardware profile, compute limits (CPU and Memory), and the NIM cluster storage size (PVC).
- **Security & Access:** Deployments can be exposed to external clients via an external route, and secured using token authentication generated for a specific Service Account.
- **Customizing Model Selection:** Administrators can control exactly which NIM models are available for deployment. By creating a **`ConfigMap`** containing specific model IDs from the NGC catalog and adding it to the **`odh-nim-account`** Account custom resource (CR), you can restrict the deployment dropdown list to a curated set of approved models.

**4. Monitoring NIM Containers** OpenShift AI provides deep visibility into NIM container performance, allowing teams to ensure their generative AI models meet strict Service Level Objectives:

- **NIM-Specific Metrics:** From the **NIM Metrics** tab of a deployed model, you can track GPU cache usage over time, current running/waiting/max request counts, tokens counts, time to first token, time per output token, and request outcomes.
- **Overall Performance Metrics:** From the **Endpoint performance** tab, you can track the number of successful/failed requests, average response time, CPU utilization, and memory utilization per model replica.
- **Legacy Enablement:** If you are upgrading from older versions to 3.0 with existing NIM deployments, administrators must manually enable metrics by adding the **`runtimes.opendatahub.io/nvidia-nim: "true"`** annotation to the **`ServingRuntime`** and Prometheus endpoint annotations (**`prometheus.io/path: "/metrics"`**, **`prometheus.io/port: "8000"`**) to the **`InferenceService`**.

---

**Relevant Official Documentation References**

You can refer your client to the following specific guides and chapters within the **Red Hat OpenShift AI Self-Managed 3.0** documentation suite for step-by-step implementation:

- **For Enabling the NIM Platform:**
  - _Document_: [**Configuring model servers on the NVIDIA NIM model serving platform**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/configuring_your_model-serving_platform/configuring_model_servers_on_the_nvidia_nim_model_serving_platform)
    - _Details:_ Outlines the exact prerequisites, NCA account requirements, and dashboard workflow to enable NIM.
- **For Running/Deploying NIM Models:**
  - _Document_: [**Deploying models on the NVIDIA NIM model serving platform**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/deploying_models/deploying_models_on_the_nvidia_nim_model_serving_platform)
    - _Details:_ Provides the step-by-step UI wizard instructions for deploying a NIM model, setting compute limits, and attaching hardware profiles.
- **For Customizing Model Lists & Monitoring:**
  - _Document_: [**Managing and monitoring models on the NVIDIA NIM model serving platform**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/managing_and_monitoring_models/managing_and_monitoring_models_on_the_nvidia_nim_model_serving_platform)
    - _Details:_ Covers how to use the **`odh-nim-account`** custom resource to customize the model selection list, as well as how to enable and view NIM metrics and graphs in the dashboard.
