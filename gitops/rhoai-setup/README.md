# RHOAI Setup

## Operator Installation

### Install required operators

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

### Install RHOAI Operator

```bash
# Install the operator subscription
until oc apply -k gitops/rhoai-setup/operators/operator-rhoai; do : ; done

# Wait for operator to be ready (3-5 minutes)
oc wait --for=condition=Ready pod -l name=rhods-operator \
  -n redhat-ods-operator --timeout=600s
```

### Create DataScienceCluster

```bash
# Deploy the RHOAI instance
oc apply -f gitops/rhoai-setup/operators/operator-rhoai/datasciencecluster.yaml

# Wait for all components to be ready (5-10 minutes)
oc wait --for=condition=Ready datasciencecluster default-dsc \
  --timeout=600s
```

#### Verification

```bash
# Check operator status
oc get csv -n redhat-ods-operator

# Check DataScienceCluster status
oc get datasciencecluster

# Check RHOAI dashboard
oc get route rhods-dashboard -n redhat-ods-applications
```

## Admin Configuration

### Configure cluster settings

```bash
until oc apply -k gitops/rhoai-setup/admin-configuration/cluster-settings; do : ; done
```

### Configure logging

```bash
until oc apply -k gitops/rhoai-setup/admin-configuration/configure-logging; do : ; done
```

### Customize dashboard (enable features)

```bash
until oc apply -k gitops/rhoai-setup/admin-configuration/customize-dashboard; do : ; done
```

### Configure NVIDIA DCGM Dashboard

```bash
until oc apply -k gitops/rhoai-setup/admin-configuration/dashboard-nvidia-dcgm; do : ; done
```

### Create hardware profiles

```bash
until oc apply -k gitops/rhoai-setup/admin-configuration/hardware-profiles; do : ; done
```

## Workbench running on CPU and GPU nodes

```bash
until oc apply -k gitops/rhoai-setup/workbench-gpu-cpu; do : ; done
```
