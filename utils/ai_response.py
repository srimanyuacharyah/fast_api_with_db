import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.getenv("GITHUB_TOKEN")

client = None
if token:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )


def get_completion(user_message, system_message="You are a helpful assistant. You were developed and built by srimanyu."):
    """
    Get a completion from the AI model.
    
    Args:
        user_message: The user's message/question
        system_message: The system prompt (default: "You are a helpful assistant.")
    
    Returns:
        The model's response
    """
    if not client:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    response = client.complete(
        messages=[
            SystemMessage(system_message),
            UserMessage(user_message),
        ],
        model=model
    )
    return response.choices[0].message.content

