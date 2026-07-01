# **Benchmark models using GuideLLM**

## What is GuideLLM?

GuideLLM is an open-source benchmarking toolkit from Red Hat designed to evaluate the performance of Large Language Model (LLM) deployments under realistic workloads. It helps organizations understand how models perform before production by measuring throughput, latency, concurrency, and resource requirements.

### Why it matters

Running an LLM in production involves balancing many variables, including:

- Model size and configuration
- Hardware selection (GPU/CPU)
- Traffic patterns
- Infrastructure costs
- Service Level Objectives (SLOs)

GuideLLM helps teams make data-driven deployment decisions instead of relying on theoretical benchmarks.

### Key Use Cases

GuideLLM supports:

1. **Pre-deployment benchmarking** – Determine whether a model and hardware combination can meet performance goals.
2. **Regression testing** – Compare performance after model, code, or infrastructure changes.
3. **Hardware evaluation** – Measure how different hardware configurations affect inference throughput.
4. **Capacity planning** – Estimate how much infrastructure is needed for expected traffic volumes.

### Architecture Highlights

GuideLLM is built with a modular architecture that supports multiple deployment scenarios. Key capabilities include:

- Flexible datasets (Hugging Face or synthetic prompts)
- OpenAI-compatible backends such as vLLM
- Customizable traffic generation
- Benchmark sweeps across load levels
- Exportable results in JSON, YAML, and CSV formats

### Traffic Simulation

The tool can simulate realistic workloads using:

- Fixed requests-per-second (RPS)
- Concurrency-based traffic
- Poisson-distributed traffic
- Ramp-up testing patterns

This allows benchmarking against actual application behavior rather than generic stress tests.

## Metrics Collected

GuideLLM captures several performance indicators that inform deployment readiness and scalability planning. [1](https://developers.redhat.com/articles/2025/06/20/guidellm-evaluate-llm-deployments-real-world-inference#)

| Metric                     | Description                               | Primary Use                |
| -------------------------- | ----------------------------------------- | -------------------------- |
| Requests Per Second (RPS)  | Number of completed requests per second   | Throughput measurement     |
| Request Latency            | End-to-end request processing time        | Responsiveness analysis    |
| Time To First Token (TTFT) | Time before first generated token appears | User experience evaluation |
| Inter-Token Latency (ITL)  | Delay between subsequent generated tokens | Generation smoothness      |
| Output Tokens/Sec          | Number of generated tokens per second     | Inference efficiency       |

All benchmark results can be exported as:

- JSON
- YAML
- CSV

---

**Relevant Official Documentation References**

- _Document:_ [**GuideLLM: Evaluate LLM Deployments for Real-World Inference**](https://developers.redhat.com/articles/2025/06/20/guidellm-evaluate-llm-deployments-real-world-inference#)
- _Github:_ [**GuideLLM Repo**](https://github.com/vllm-project/guidellm)
