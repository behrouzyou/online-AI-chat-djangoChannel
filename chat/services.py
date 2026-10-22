import json
import os

import httpx

OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def ask_ai(message):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": message}],
        "stream": True,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream("POST", OPEN_ROUTER_URL, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue

                chunk_data = line[6:]
                if chunk_data == "[DONE]":
                    break

                try:
                    chunk = json.loads(chunk_data)
                except json.JSONDecodeError:
                    continue

                choices = chunk.get("choices", [])
                if not choices:
                    continue

                delta = choices[0].get("delta", {})
                text = delta.get("content")
                if text:
                    yield text
