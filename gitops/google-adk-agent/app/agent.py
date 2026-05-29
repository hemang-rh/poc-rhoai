import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


def create_agent() -> LlmAgent:
    model_name = os.getenv("ADK_MODEL_NAME", "openai/gpt-oss-120b")
    agent_name = os.getenv("AGENT_NAME", "gpt_oss_120b_agent")
    description = os.getenv(
        "AGENT_DESCRIPTION",
        "Simple Google ADK agent backed by GPT OSS 120B on OpenShift AI.",
    )
    instruction = os.getenv(
        "AGENT_INSTRUCTION",
        "You are a concise and helpful assistant running on OpenShift AI.",
    )

    return LlmAgent(
        model=LiteLlm(model=model_name),
        name=agent_name,
        description=description,
        instruction=instruction,
    )


root_agent = create_agent()
