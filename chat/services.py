import httpx
import json


OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def ask_ai(message):
    api_key = "your api key from open router .ai"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"}
    data = {"model":"openrouter/free", "messages":[{"role":"user", "content": message}], "stream":True}

    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream("POST", OPEN_ROUTER_URL, headers=headers, json=data) as response:
            async for line in response.aiter_lines():
                if not line: continue
                if not line.startswith("data: "): continue

                data = line[6:]
                if data == "[DONE]": break

                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue

                choices = chunk.get("choices", [])
                if not choices: continue

                delta = choices[0].get("delta", {})
                content = delta.get("content")

                if content:
                    yield content
