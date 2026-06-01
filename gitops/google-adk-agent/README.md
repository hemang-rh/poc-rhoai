# Google ADK Agent

This folder deploys a small Google ADK agent on OpenShift and points it at an
OpenAI-compatible GPT OSS 120B endpoint already running in OpenShift AI.

## Configure

Edit `configmap.yaml` if your served model name or endpoint differs:

- `ADK_MODEL_NAME`: LiteLLM model string. Keep the `openai/` provider prefix
  for an OpenAI-compatible endpoint, for example
  `openai/redhataillama-31-8b-instruct`.
- `OPENAI_API_BASE`: Internal OpenShift service URL ending in `/v1`.

If your endpoint requires authentication, set `OPENAI_API_KEY` in
`secret.example.yaml`.

## Build and Push the Image

```bash
podman build --platform linux/amd64 \
  -t quay.io/rh-ee-hshishir/google-adk-agent:2.0 \
  gitops/google-adk-agent/app

podman login quay.io
podman push quay.io/rh-ee-hshishir/google-adk-agent:2.0
```

Update `deployment.yaml` if you use a different Quay repository or tag.
If the cluster cannot pull from Quay, mirror this image into a registry
the cluster can access and use that mirrored image reference instead.

If the pod fails with `Exec format error`, confirm the node architecture and
rebuild for that platform:

```bash
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.nodeInfo.architecture}{"\n"}{end}'
```

## Deploy

```bash
oc apply -k gitops/google-adk-agent
```

The deployment uses the prebuilt image, so the OpenShift pod does not need
internet access to run `pip install`.

## Making changes and redeploying

```bash
oc apply -k gitops/google-adk-agent
oc -n google-adk-agent rollout restart deployment/google-adk-agent
```

## Test

```bash
oc -n google-adk-agent get pods
oc -n google-adk-agent get route google-adk-agent

curl -k "https://$(oc -n google-adk-agent get route google-adk-agent -o jsonpath='{.spec.host}')/healthz"

curl -k "https://$(oc -n google-adk-agent get route google-adk-agent -o jsonpath='{.spec.host}')/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"Say hello from the GPT OSS 120B backed ADK agent."}'
```
