# LLM Fundamentals

A hands-on Python repository for learning the core concepts behind modern LLM applications.

This project demonstrates how to work with large language models using OpenAI, Google Gemini, and Ollama, covering the essentials of:

- basic LLM calls
- multi-turn conversations
- system prompts and generation settings
- structured outputs
- tool calling
- provider-specific integrations

## Why this repository?

The goal is to make the fundamentals practical and easy to understand. Instead of abstract theory, each example is a small, runnable Python script that shows the key pattern you need in real applications.

## Repository structure

- `1_llm_basics.py` — basic OpenAI Responses API usage
- `1_llm_basics_gemini.py` — basic Gemini usage
- `1_llm_basics_ollama.py` — basic Ollama usage
- `2_structured_outputs.py` — generating validated structured data with Pydantic
- `2_structured_outputs_ollama.py` — structured outputs with Ollama
- `3_tool_calls.py` — OpenAI function/tool calling example
- `3_tool_calls_ollama.py` — tool calling using Ollama
- `3_tool_calls_intent_based_ollama.py` — intent-based tool orchestration example
- `3_tool_calls_sequence_based_ollama.py` — sequence-based tool orchestration example

## Learning path

### 1. LLM basics

Understand how to:

- send a simple prompt
- configure model behavior
- maintain conversation history
- stream output
- inspect usage metadata

### 2. Structured outputs

Learn how to constrain model responses to a specific schema using Pydantic models so they can be parsed safely in Python.

### 3. Tool calling

Learn how LLMs can decide when to call functions and use those results to answer questions with up-to-date or domain-specific data.

## Prerequisites

- Python 3.10+
- A virtual environment is recommended
- API access to one or more providers:
  - OpenAI
  - Google Gemini
  - Ollama (local models)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tarang2801/llm_fundamental.git
   cd llm_fundamental
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # or
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install openai python-dotenv pydantic google-genai ollama
   ```

4. Create a `.env` file for API keys if needed:

   ```env
   OPENAI_API_KEY=your_openai_key
   GOOGLE_API_KEY=your_google_api_key
   ```

5. Run any example script:

   ```bash
   python 1_llm_basics.py
   ```

## Provider notes

### OpenAI

The scripts using `OpenAI` rely on the OpenAI Python SDK and the `OPENAI_API_KEY` environment variable.

### Gemini

The Gemini examples use the Google GenAI SDK and require a Google API key.

### Ollama

Ollama examples assume a local Ollama server is running and that a model such as `llama3.2` is available.

## Example usage

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="What is the square root of 49?"
)

print(response.output_text)
```

## Notes

This repository is intended as a learning resource and reference implementation for the fundamentals of LLM application development. It is intentionally lightweight and focused on clarity over complexity.

## License

This project does not currently declare a license. If you plan to reuse or distribute it, consider adding one such as MIT or Apache 2.0.

## Contributing

Feel free to fork the repository, experiment with the examples, and extend the scripts with additional patterns such as:

- retrieval-augmented generation (RAG)
- agent workflows
- evaluation and testing
- streaming UI patterns
- memory systems
