import json
import os
from dotenv import load_dotenv, find_dotenv
import requests




load_dotenv(find_dotenv())
api_key = os.getenv("ASI_API_KEY")
if not api_key:
    raise ValueError("ASI_API_KEY not found in .env")


def llmChat(messages, model="asi1-mini", max_tokens=8000, temperature=0, stream=False):
    url = "https://api.asi1.ai/v1/chat/completions"
    # Convert LangChain Message objects to dicts
    if hasattr(messages[0], 'type'):  # Detects if these are LangChain messages
        messages = [{"role": m.type, "content": m.content} for m in messages]
        
    # Map any non-standard roles to OpenAI-style roles
    role_map = {
        "human": "user",
        "user": "user",
        "ai": "assistant",
        "assistant": "assistant",
        "system": "system"
    }
    
    formatted_messages = []
    for m in messages:
        # Determine the original role and content
        if isinstance(m, dict):
            orig_role = m.get("role", "").lower()
            content = m.get("content", "")
        else:
            orig_role = getattr(m, "type", "").lower()
            content = getattr(m, "content", "")

        # Map to valid role or default to "user"
        role = role_map.get(orig_role, "user")

        formatted_messages.append({"role": role, "content": content})
    payload = json.dumps({
        "model": model,
        "messages": formatted_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {api_key}"
    }

    response = requests.post(url, headers=headers, data=payload, timeout=100)
    print("Status:", response.status_code)
    # print("Response:", response.text)
    
    return response.text
