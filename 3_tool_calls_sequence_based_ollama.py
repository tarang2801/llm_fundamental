import ollama
import json


# ------------------------------------------------
# 1. Actual tools
# ------------------------------------------------

def get_weather(city: str):
    # Imagine this calls a real weather API
    return {
        "success": True,
        "city": city,
        "temperature": 28,
        "unit": "celsius",
        "condition": "sunny"
    }


def get_airQualityIndex(city: str):
    # Imagine this calls a real AQI API
    return {
        "success": True,
        "city": city,
        "aqi": 300,
        "unit": "AQI",
        "condition": "Worst"
    }


# ------------------------------------------------
# 2. Tool definitions
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
            "description": "Get the current AQI for a given city",
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
# 3. User query
# ------------------------------------------------

user_query = "What is the current AQI in Delhi?"


# ------------------------------------------------
# 4. Let the LLM understand the request
# ------------------------------------------------

messages = [
    {
        "role": "system",
        "content": """
        You are an assistant that answers weather and air quality questions.

        For AQI questions:
        - The application will always get weather information first.
        - The application will then get AQI information.
        - Do not try to bypass this sequence.
        """
    },
    # {
    #     "role": "system",
    #     "content": """
    #     You are an assistant that answers weather and air quality questions.

    #     For AQI questions:
    #     - The application will always get weather information first.
    #     - The application will then get AQI information.
    #     - The application will then give both results to you to generate a final response.
    #     - Do not try to bypass this sequence.
    #     """
    # },
    {
        "role": "user",
        "content": user_query
    }
]


response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=tools
)


# ------------------------------------------------
# 5. Determine what the user is asking
# ------------------------------------------------

tool_calls = response["message"].get("tool_calls", [])

if tool_calls:

    tool_call = tool_calls[0]

    function_name = tool_call["function"]["name"]
    function_args = tool_call["function"]["arguments"]

    print(f"LLM wants to call: {function_name}")


    # ------------------------------------------------
    # 6. AQI workflow
    # ------------------------------------------------

    if function_name == "get_airQualityIndex":

        city = function_args["city"]

        print(f"\n🌤️ Step 1: Getting weather for {city}")

        weather_result = get_weather(city)

        print(f"Weather result: {weather_result}")


        # ------------------------------------------------
        # 7. Check weather success
        # ------------------------------------------------

        if weather_result.get("success") is not True:

            print("❌ Weather API failed.")

            final_response = ollama.chat(
                model="llama3.2",
                messages=[
                    *messages,
                    {
                        "role": "user",
                        "content": "The weather lookup failed. Tell the user that the AQI cannot be retrieved."
                    }
                ]
            )

            print(final_response["message"]["content"])

        else:

            print(f"\n🌫️ Step 2: Getting AQI for {city}")

            aqi_result = get_airQualityIndex(city)

            print(f"AQI result: {aqi_result}")


            # ------------------------------------------------
            # 8. Give both results to the LLM
            # ------------------------------------------------

            messages.append(response["message"])

            messages.append({
                "role": "tool",
                "content": json.dumps(weather_result)
            })

            messages.append({
                "role": "tool",
                "content": json.dumps(aqi_result)
            })


            # ------------------------------------------------
            # 9. Generate final response
            # ------------------------------------------------

            final_response = ollama.chat(
                model="llama3.2",
                messages=messages
            )

            print(
                f"\n💬 Final answer:\n"
                f"{final_response['message']['content']}"
            )


    # ------------------------------------------------
    # 10. Normal weather request
    # ------------------------------------------------

    elif function_name == "get_weather":

        city = function_args["city"]

        weather_result = get_weather(city)

        messages.append(response["message"])

        messages.append({
            "role": "tool",
            "content": json.dumps(weather_result)
        })

        final_response = ollama.chat(
            model="llama3.2",
            messages=messages
        )

        print(
            f"\n💬 Final answer:\n"
            f"{final_response['message']['content']}"
        )

else:

    print(
        "\n💬 Final answer:\n"
        f"{response['message']['content']}"
    )