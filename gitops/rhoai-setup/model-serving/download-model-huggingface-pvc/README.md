# Model Downloader Pod (OpenShift)

This folder contains OpenShift manifests to download a Hugging Face model into a PVC.

## Resources

- `pvc-model-download.yaml`: Persistent storage for downloaded models.
- `configmap-model-download.yaml`: Non-secret settings (`MODEL_ID`, `REVISION`, `DOWNLOAD_DIR`).
- `secret-hf-token.example.yaml`: Secret template for `HF_TOKEN`.
- `pod-model-downloader.yaml`: One-shot pod that performs the download.
- `kustomization.yaml`: Applies all resources together.

## Prerequisites

- Logged in to OpenShift (`oc login ...`).
- Target project selected (`oc project <your-project>`).

## Configure

1. Edit `secret-hf-token.example.yaml` and set `HF_TOKEN`.
2. Edit `configmap-model-download.yaml` and set `MODEL_ID`.
3. Optional: change PVC size/storage class in `pvc-model-download.yaml`.

## Deploy

```bash
oc apply -k gitops/rhoai-setup/model-serving/download-model-pvc
```

## Monitor

```bash
oc get pod model-downloader -w
oc logs -f pod/model-downloader
```

## Verify files in PVC

The model is downloaded under:

- `/<MODEL_ID with '/' replaced by '_'>`
