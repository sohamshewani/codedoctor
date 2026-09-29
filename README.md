# CodeDoctor CLI 🩺⚡

An autonomous terminal debugging assistant powered by **Qwen 2.5 (7B)** running locally via **Ollama**.

## What it does
- Executes Python target scripts in an isolated subprocess.
- Automatically catches runtime exceptions, traces, and crashes.
- Relays the exact traceback and failing code to local Qwen 2.5 for instant diagnosis and patches without API fees or sending code to external servers.

## Prerequisites
- [Ollama](https://ollama.ai) installed.
- Pull the model:
  ```bash
  ollama run qwen2.5:7b
