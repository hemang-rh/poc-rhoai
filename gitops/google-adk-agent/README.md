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

## Deploy

```bash
oc apply -k gitops/google-adk-agent
```

The default deployment runs the Python source directly from
`source-configmap.yaml` so the app can be created with `oc apply` only.

If you apply individual files instead of using Kustomize, create the namespace,
`configmap.yaml`, `source-configmap.yaml`, and `secret.example.yaml` before
`deployment.yaml`.

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
