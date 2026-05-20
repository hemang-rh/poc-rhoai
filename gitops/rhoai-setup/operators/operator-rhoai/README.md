# Red Hat OpenShift AI (RHOAI) Operator

This directory contains the configuration for deploying Red Hat OpenShift AI operator and creating a DataScienceCluster instance.

## Overview

Red Hat OpenShift AI (RHOAI) is an enterprise AI/ML platform that provides:

- **Dashboard**: Web UI for data scientists and ML engineers
- **Workbenches**: Jupyter notebooks and development environments
- **Model Serving**: Deploy models with KServe and ModelMesh
- **Pipelines**: Build and orchestrate ML workflows
- **Distributed Training**: Scale training across multiple nodes

## RHOAI 3.x Deployment

### Subscription Channel

RHOAI 3.x is currently deployed using the **`stable-3.x`** subscription channel.

### Required Dependencies

RHOAI 3.x requires the following operators to be installed **before** the RHOAI operator:

1. **Node Feature Discovery (NFD) Operator**
   - Detects hardware features on nodes
   - Required for GPU discovery and labeling
2. **NVIDIA GPU Operator**
   - Enables GPU workload scheduling on OpenShift
   - Required for AI workload scheduling on NVIDIA GPU nodes

### Optional Dependencies

For enhanced GPU support and monitoring:

3. **NVIDIA DCGM Operator** (GPU Operator)
   - Provides GPU health monitoring and telemetry
   - Recommended if using NVIDIA GPUs

## Deployment

### Manual Deployment with Kustomize

#### Step 1: Install required operators

```bash
# Deploy NFD operator
until oc apply -k gitops/rhoai-setup/operators/operator-nfd; do : ; done

# Wait for operators to be ready (2-3 minutes)
oc -n openshift-nfd wait pod --all \
  --for=condition=Ready \
  --timeout=300s
```

```bash
# Deploy NVIDIA GPU operator
until oc apply -k gitops/rhoai-setup/operators/operator-nvidia-gpu; do : ; done

# Wait for the operator to be ready (this can take 1-2 minutes)
oc wait --for=condition=available --timeout=300s \
  deployment/gpu-operator -n nvidia-gpu-operator

# Wait for CRD to be installed
oc wait --for condition=established --timeout=60s \
  crd/clusterpolicies.nvidia.com

# Now apply the ClusterPolicy
oc apply -f gitops/rhoai-setup/operators/operator-nvidia-gpu/clusterpolicy.yaml

# Wait for
oc wait --for=condition=Ready pod -l app=nvidia-operator-validator \
  -n nvidia-gpu-operator --timeout=300s

```

#### Step 2: Install RHOAI Operator

```bash
# Install the operator subscription
until oc apply -k gitops/rhoai-setup/operators/operator-rhoai; do : ; done

# Wait for operator to be ready (3-5 minutes)
oc wait --for=condition=Ready pod -l name=rhods-operator \
  -n redhat-ods-operator --timeout=600s
```

#### Step 3: Create DataScienceCluster

```bash
# Deploy the RHOAI instance
oc apply -f gitops/rhoai-setup/operators/operator-rhoai/datasciencecluster.yaml

# Wait for all components to be ready (5-10 minutes)
oc wait --for=condition=Ready datasciencecluster default-dsc \
  --timeout=600s
```

### Verification

```bash
# Check operator status
oc get csv -n redhat-ods-operator

# Check DataScienceCluster status
oc get datasciencecluster

# Check RHOAI dashboard
oc get route rhods-dashboard -n redhat-ods-applications
```

## Configuration

### Changing the Subscription Channel

Edit `kustomization.yaml` and update the patch value:

```yaml
patches:
  - target:
      kind: Subscription
      name: rhods-operator
    patch: |-
      - op: replace
        path: /spec/channel
        value: fast-3.x
```

Then apply the changes:

```bash
oc apply -k platform/rhoai-operator/base/
```

**Available channels:**

- `stable-3.x` - Production-ready releases (use after 3.2 release)
- `fast-3.x` - Latest features across all versions

### Customizing DataScienceCluster Components

Edit `datasciencecluster.yaml` to enable/disable components:

```yaml
spec:
  components:
    dashboard:
      managementState: Managed # Enable
    workbenches:
      managementState: Managed # Enable
    kserve:
      managementState: Managed # Enable model serving
    modelmeshserving:
      managementState: Managed # Enable ModelMesh
    datasciencepipelines:
      managementState: Managed # Enable pipelines
    codeflare:
      managementState: Removed # Disable distributed training
    ray:
      managementState: Removed # Disable KubeRay (defaults to Managed in instance/datasciencecluster.yaml)
    kueue:
      managementState: Removed # Use external Kueue operator
    trainingoperator:
      managementState: Removed # Disable Kubeflow Training Operator
    trainer:
      managementState: Removed # Disable Kubeflow Trainer v2 (defaults to Managed in instance/datasciencecluster.yaml)
    trustyai:
      managementState: Removed # Disable TrustyAI
```

Available states:

- `Managed` - Component is deployed and managed
- `Removed` - Component is not deployed

## Configuring Operator Logger

You can change the log level for OpenShift AI Operator components by setting the .spec.devFlags.logmode flag for the DSC Initialization/DSCI custom resource during runtime. If you do not set a logmode value, the logger uses the INFO log level by default.

Available log levels:

- `devel` or `development` (Stacktrace level = WARN, Verbosity = INFO, Output = Console)
- `prod` or `production` (Stacktrace level = ERROR, Verbosity = INFO, Output = JSON)

```bash
oc patch dsci default-dsci -p '{"spec":{"devFlags":{"logmode":"development"}}}' --type=merge
```

## Accessing RHOAI Dashboard

```bash
# Get the dashboard URL
RHOAI_URL=$(oc get route rhods-dashboard \
  -n redhat-ods-applications -o jsonpath='{.spec.host}')
echo "RHOAI Dashboard: https://${RHOAI_URL}"

# Login with your OpenShift credentials
```

## Troubleshooting

### Check Operator Installation

```bash
# Check subscription
oc get subscription rhods-operator -n redhat-ods-operator

# Check CSV (ClusterServiceVersion)
oc get csv -n redhat-ods-operator

# Check operator pods
oc get pods -n redhat-ods-operator

# Check operator logs
oc logs -l name=rhods-operator -n redhat-ods-operator
```

### Check DataScienceCluster Status

```bash
# Get cluster status
oc describe datasciencecluster default-dsc

# Check component status
oc get pods -n redhat-ods-applications
oc get pods -n redhat-ods-monitoring

# Check dashboard status
oc get deployment rhods-dashboard -n redhat-ods-applications
```

### Common Issues

**Operator stuck in "Installing":**

- Check install plan: `oc get installplan -n redhat-ods-operator`
- Check operator logs for errors
- Ensure dependencies (NFD, Kueue) are installed first

**DataScienceCluster not ready:**

- Check operator is running: `oc get pods -n redhat-ods-operator`
- Check for failed pods: `oc get pods -A | grep Error`
- Review DataScienceCluster status: `oc describe datasciencecluster default-dsc`

**Dashboard not accessible:**

- Check route exists: `oc get route -n redhat-ods-applications`
- Verify dashboard deployment: `oc get deployment rhods-dashboard -n redhat-ods-applications`
- Check pod logs: `oc logs -l app=rhods-dashboard -n redhat-ods-applications`

## Version Compatibility

| RHOAI Version | OpenShift Version | Subscription Channel |
| ------------- | ----------------- | -------------------- |
| 3.4 (current) | 4.19+             | stable-3.x           |
