import ollama
import json


# ------------------------------------------------
# 0. The problem - model has no access to real-time data
# ------------------------------------------------

# Without a tool, the model cannot actually call your
# get_weather() Python function.


# ------------------------------------------------
# 1. Define the actual Python function
# ------------------------------------------------

def get_weather(city: str):
    return {
        "city": city,
        "temperature": 28,
        "unit": "celsius",
        "condition": "sunny"
    }

def get_airQualityIndex(city: str):
    return {
        "city": city,
        "aqi": 300,
        "unit": "AQI",
        "condition": "Worst"
    }

# ------------------------------------------------
# 2. Describe the function to the model
# ------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_airQualityIndex",
            "description": "Get the current air quality index (AQI) for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get air quality for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# ------------------------------------------------
# 3. Step 1 - Send question + tools to the model
# ------------------------------------------------

messages = [
    {
        "role": "user",
        "content": "What is the current aqi in Delhi?"
    }
]


response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=tools
)


# ------------------------------------------------
# 4. Inspect the response
# ------------------------------------------------

print("Full model response:")
print(response)


# ------------------------------------------------
# 5. Check whether the model wants to call a tool
# ------------------------------------------------

if response["message"].get("tool_calls"):

    tool_call = response["message"]["tool_calls"][0]

    function_name = tool_call["function"]["name"]
    function_args = tool_call["function"]["arguments"]

    print(
        f"\n🔧 Tool called: "
        f"{function_name}("
        f"{', '.join(f'{k}={v}' for k, v in function_args.items())}"
        f")"
    )


    # ------------------------------------------------
    # 6. Run the Python function ourselves
    # ------------------------------------------------

    if function_name == "get_weather":

        function_result = get_weather(
            function_args["city"]
        )
        print(f"📦 Raw result: {function_result}")

    elif function_name == "get_airQualityIndex":

        function_result = get_airQualityIndex(
            function_args["city"]
        )

        print(f"📦 Raw result: {function_result}")


    # ------------------------------------------------
    # 7. Add the assistant's tool call to history
    # ------------------------------------------------

    messages.append(response["message"])


    # ------------------------------------------------
    # 8. Add the tool result to history
    # ------------------------------------------------

    messages.append(
        {
            "role": "tool",
            "content": json.dumps(function_result)
        }
    )


    # ------------------------------------------------
    # 9. Send everything back to the model
    # ------------------------------------------------

    final_response = ollama.chat(
        model="llama3.2",
        messages=messages,
        tools=tools
    )


    # ------------------------------------------------
    # 10. Final answer
    # ------------------------------------------------

    print(
        f"\n💬 Final answer: "
        f"{final_response['message']['content']}"
    )

else:

    print(
        "\n💬 Model answered directly:"
        f"\n{response['message']['content']}"
    )