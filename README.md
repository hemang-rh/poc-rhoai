# RHOAI POC Setup

## Summary

This repository provides **automated setup and configuration tools for deploying Red Hat OpenShift AI (RHOAI) on OpenShift clusters**. It's designed to streamline the process of setting up a complete AI/ML platform with GPU support and related infrastructure.

## Pre-Requisites

Before using this repository, ensure you have the following:

- **Cluster running OpenShift 4.19+** with cluster-admin access
- **`oc` CLI** installed and configured
- **GPU node(s)** (optional, for model serving and training)
- `ansible-playbook` installed
- `jq` installed

**Prerequisites Check:**

```bash
# Verify OpenShift version (4.19+ required)
oc version

# Verify cluster-admin access
oc whoami
oc auth can-i create namespace

# Verify ansible-playbook is installed
ansible-playbook --version

# Verify jq is installed
jq --version
```

### How to install ansible playbook

- For macOS:

  ```sh
  brew install ansible
  ```

- For Linux:
  - Using pip (if Python is installed):
    ```sh
    pip install --user ansible
    ```
  - For Debian/Ubuntu:
    ```sh
    sudo apt update
    sudo apt install ansible
    ```
  - For RHEL/CentOS/Fedora:
    ```sh
    # For Fedora
    sudo dnf install ansible
    # For RHEL/CentOS
    sudo yum install ansible
    ```

- For Windows:
  - Using pip (if Python is installed):
    ```sh
    pip install --user ansible
    ```
  - Using WSL (Windows Subsystem for Linux):
    ```sh
    # Install Ansible inside WSL (Ubuntu/Debian)
    sudo apt update
    sudo apt install ansible
    ```
- Verify installation:
  ```sh
  ansible --version
  ansible-playbook --version
  ```

### How to install OpenShift CLI (`oc`)

- Install the OpenShift CLI
  - [Official documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/cli_tools/openshift-cli-oc#cli-getting-started).
  - Download for Windows [Link](https://downloads-openshift-console.apps.cluster-wfp7h.wfp7h.sandbox1962.opentlc.com/amd64/windows/oc.zip)
  - Download for Linux, Mac, Windows [LINK](https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-4.20/)

- Verify installation:
  ```sh
  oc version
  ```

---
