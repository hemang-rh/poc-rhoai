# **OpenShift AI: Hardware Profiles Guide**

**1. Overview of Hardware Profiles:** Hardware profiles are custom resources (CRs) designed for targeted scheduling \***\*within Red Hat OpenShift AI. Introduced in OpenShift AI 3.0, they provide a flexible, consistent way to define compute configurations for AI workloads, completely **replacing the legacy Accelerator Profiles and Container Size selectors\*\*.

By using hardware profiles, administrators can manage and allocate specific compute resources—such as hardware accelerators (like NVIDIA/AMD GPUs, Intel Gaudi, or IBM Spyre), specialized memory, or CPU-only nodes—specifically tailored for model serving and workbenches.

**2. Key Capabilities and Business Value** Hardware profiles offer fine-grained control over resource allocation and ensure workloads are routed precisely to the infrastructure they need, reducing waste and maximizing hardware ROI. Their specifications include:

- **Explicit Resource Limits:** You can define guaranteed minimums (requests) and maximums (limits) for CPUs, memory, and specific accelerators within the profile.
- **Intelligent Node Placement:** While legacy features relied mostly on taints, hardware profiles utilize **node selectors and tolerations** to guarantee that workloads land exactly on the designated worker nodes. This is especially important for directing specific large language models (LLMs) to specialized nodes (e.g., nodes configured with specific GPU time-slicing or Multi-Instance GPU strategies).
- **CPU-Only and Accelerator Flexibility:** Hardware profiles support both accelerator-driven and CPU-only configurations out-of-the-box.

**3. Workload Allocation and Queueing (Kueue Integration)** Hardware profiles seamlessly integrate with the Red Hat build of Kueue to manage cluster quotas and priorities dynamically:

- **Local Queue Assignment:** You can assign a hardware profile to a **`LocalQueue`**. Workloads using this profile are automatically queued and managed based on workload priority when cluster resources are limited.
- **Priority Tiers:** Administrators can select a "Workload priority" within the profile, ensuring that higher-priority financial modeling or production inference workloads are admitted before lower-priority development jobs.

**4. Profile Visibility and Scope** To maintain strict governance and organization across different teams, hardware profiles can be scoped according to your security boundaries:

- **Global Visibility (Visible Everywhere):** The profile can be accessed and used across all areas and projects within OpenShift AI.
- **Project-Scoped (Limited Visibility):** The profile is restricted, limiting the areas and specific data science projects where users are permitted to utilize that specific hardware configuration.

---

**Relevant Official Documentation References**

Because OpenShift AI documentation is updated iteratively, you can refer your client to the following specific guides and chapters within the **Red Hat OpenShift AI Self-Managed 3.0** documentation suite for step-by-step implementation:

- **For Creating and Managing Profiles:**
  - _Document:_ [**Working with hardware profiles**](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/html/working_with_accelerators/working-with-hardware-profiles_accelerators)
    - _Details:_ Covers the step-by-step UI workflow for creating, updating, and deleting hardware profiles, as well as configuring node selectors, tolerations, and visibility scopes.
