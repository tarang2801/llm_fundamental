import ollama


# ------------------------------------------------
# 1. Simplest possible API call
# ------------------------------------------------

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the square root of 49?"
#         }
#     ]
# )

# print(response["message"]["content"])


# # ------------------------------------------------
# # 4. Multi-turn conversation
# # ------------------------------------------------

# messages = [
#     {
#         "role": "user",
#         "content": "My name is Harish"
#     },
#     {
#         "role": "assistant",
#         "content": "Nice to meet you Harish!"
#     },
#      {
#         "role": "user",
#         "content": "what is my name?"
#     }
# ]

# response = ollama.chat(
#     model="llama3.2",
#     messages=messages
# )

# print(response["message"]["content"])


# # ------------------------------------------------
# # 5. System prompt + temperature + max tokens
# # ------------------------------------------------

# response = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant who makes jokes."
#         },
#         {
#             "role": "user",
#             "content": "What is the square root of 49?"
#         }
#     ],
#     options={
#         "temperature": 0.7,
#         "num_predict": 100
#     }
# )

# print(response["message"]["content"])


# # ------------------------------------------------
# # 6. Token usage
# # ------------------------------------------------

# print("Prompt tokens:", response.get("prompt_eval_count"))
# print("Response tokens:", response.get("eval_count"))


# # ------------------------------------------------
# # 7. Streaming
# # ------------------------------------------------

stream = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Tell me a short story about a robot."
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()