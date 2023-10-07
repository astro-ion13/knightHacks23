import semantic_kernel as sk
kernel = sk.Kernel()
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

api_key = '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'

kernel.add_chat_service(
    "OpenAI_chat_gpt",
    OpenAIChatCompletion(
        "gpt-3.5-turbo",
        api_key
    )
)