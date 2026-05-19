# OpenShift PVC Verification Test

This repo contains a simple OpenShift storage validation test. The goal is to verify that a PVC can be created against a chosen `StorageClass`, bind to a PV, mount into a pod, and allow basic file I/O from inside the container.

This is especially useful when testing local-storage-backed classes before using them for higher-level workloads. One important nuance is that local volumes can work for PVC-backed workloads even though Red Hat distinguishes them from classic dynamic provisioning behavior.

## Files

```text
kustomization.yaml
namespace.yaml
pvc.yaml
pod.yaml
README.md
```

## Before you run it

- Make sure you are logged in with `oc login`.
- Update `storageClassName` in `pvc.yaml` to the storage class you want to test.
- If your cluster is disconnected, replace the test image in `pod.yaml` with one available in your internal registry.

## Run the test

Apply the manifests:

```bash
until oc apply -k gitops/basic-testing/pvc-test; do : ; done
```

Check the PVC:

```bash
oc get pvc -n pvc-test
oc describe pvc test-pvc -n pvc-test
```

Check the pod:

```bash
oc get pod -n pvc-test
oc get pod pvc-test-pod -n pvc-test -o wide
```

Write a file into the mounted path:

```bash
oc exec -n pvc-test pvc-test-pod -- /bin/sh -c 'echo "OpenShift PVC test successful" > /mnt/testdata/hello.txt && sync'
```

Read it back:

```bash
oc exec -n pvc-test pvc-test-pod -- /bin/sh -c 'cat /mnt/testdata/hello.txt'
```

Expected output:

```text
OpenShift PVC test successful
```

## Interpret the result

- PVC `Bound` + pod `Running` + successful file write/read means the storage class is usable for basic PVC-backed workloads.
- PVC `Pending` means no suitable PV was found or provisioned for the claim.
- Pod `Pending` after PVC bind usually points to scheduling, node affinity, or image issues.

## Clean up

```bash
oc delete -k .
```
