from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client()


# ------------------------------------------------
# 1. Simplest possible API call
# ------------------------------------------------

# result = client.models.generate_content(
#     model="gemini-3.8-flash",
#     contents="What is the square root of 49?"
# )

# print(result.text)


# ------------------------------------------------
# 2. What does the full response object look like?
# ------------------------------------------------

# print(result)


# ------------------------------------------------
# 2.5. Raw JSON response
# ------------------------------------------------

# print(result.model_dump_json(indent=2))


# ------------------------------------------------
# 3. Extract just the text
# ------------------------------------------------

# print(result.text)


# ------------------------------------------------
# 4. Multi-turn conversation
# ------------------------------------------------

# chat = client.chats.create(
#     model="gemini-3.8-flash",
#     history=[
#         types.Content(
#             role="user",
#             parts=[types.Part(text="My name is Harish")]
#         ),
#         types.Content(
#             role="model",
#             parts=[types.Part(text="Nice to meet you Harish!")]
#         )
#     ]
# )

# response = chat.send_message(
#     message="What is my name?"
# )

# print(response.text)


# ------------------------------------------------
# 5. System prompt + temperature + max tokens
# ------------------------------------------------

result = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What is the square root of 49?",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant who makes jokes.",
        temperature=0.7,
        max_output_tokens=100
    )
)

print(result.text)


# ------------------------------------------------
# 6. Token usage
# ------------------------------------------------

# print(result.usage_metadata)


# ------------------------------------------------
# 7. Streaming
# ------------------------------------------------

# stream = client.models.generate_content_stream(
#     model="gemini-3.8-flash",
#     contents="Tell me a short story about a robot."
# )

# for chunk in stream:
#     print(chunk.text, end="", flush=True)