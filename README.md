# Online AI Chat — Django Channels

A Django Channels application that streams AI-generated responses to a browser over a WebSocket connection.

## Features
- WebSocket chat connection
- Connection confirmation for the client
- Accepts user messages and streams response chunks
- Sends start, chunk, end, and error events
- Asynchronous service calling the OpenRouter chat-completions API

## Stack
- Python and Django
- Django Channels and Daphne
- HTTPX
- OpenRouter API

## Run locally
Install the dependencies used by the project and set `OPENROUTER_API_KEY` in your environment. Then run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

## Security and reliability
Never hardcode API keys. Configure allowed hosts and WebSocket origin validation before deployment, and avoid returning internal exception details to users in production.
