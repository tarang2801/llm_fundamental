import ollama
import json

from pydantic import BaseModel
from typing import Literal


# ==================================================
# 1. Intent model
# ==================================================

class UserIntent(BaseModel):
    intent: Literal["WEATHER", "AQI", "UNKNOWN"]
    city: str | None = None


# ==================================================
# 2. Actual tools
# ==================================================

def get_weather(city: str):

    return {
        "success": True,
        "city": city,
        "temperature": 28,
        "unit": "celsius",
        "condition": "sunny"
    }


def get_airQualityIndex(city: str):

    return {
        "success": True,
        "city": city,
        "aqi": 300,
        "unit": "AQI",
        "condition": "Worst"
    }


# ==================================================
# 3. Intent detection
# ==================================================

def detect_intent(user_query):

    response = ollama.chat(
        model="llama3.2",

        messages=[
            {
                "role": "system",
                "content": """
                Determine the user's intent.

                Allowed intents:

                WEATHER
                AQI
                UNKNOWN

                Extract the city if present.
                """
            },
            {
                "role": "user",
                "content": user_query
            }
        ],

        format=UserIntent.model_json_schema()
    )

    return UserIntent.model_validate_json(
        response["message"]["content"]
    )


# ==================================================
# 4. Workflow
# ==================================================

def handle_weather(city):

    weather = get_weather(city)

    return {
        "weather": weather
    }


def handle_aqi(city):

    # Mandatory dependency

    print("1️⃣ Calling weather...")

    weather = get_weather(city)

    if not weather["success"]:

        return {
            "success": False,
            "message": "Weather service failed."
        }

    print("2️⃣ Weather succeeded")

    print("3️⃣ Calling AQI...")

    aqi = get_airQualityIndex(city)

    if not aqi["success"]:

        return {
            "success": False,
            "message": "AQI service failed."
        }

    return {
        "success": True,
        "weather": weather,
        "aqi": aqi
    }

# ==================================================
# 4.1 Generate final response
# ==================================================

def generate_final_response(user_query, result):

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "Answer the user using only the supplied data."
            },
            {
                "role": "user",
                "content": f"""
                User query:
                {user_query}

                Tool results:
                {json.dumps(result)}
                """
            }
        ]
    )

    return response["message"]["content"]

# ==================================================
# 5. Main orchestrator
# ==================================================

def handle_request(user_query):

    intent = detect_intent(user_query)

    print("Detected intent:")
    print(intent)

    if intent.intent == "WEATHER":

        return handle_weather(intent.city)

    elif intent.intent == "AQI":

        return handle_aqi(intent.city)

    else:

        return {
            "success": False,
            "message": "I don't understand the request."
        }


# ==================================================
# 6. Test
# ==================================================

query = "What is the current AQI in Delhi?"
result = handle_request(query)

print("\nFinal result:")
print(json.dumps(result, indent=2))
print("\nFinal answer:")
final_answer = generate_final_response(
    query,
    result
)
print(final_answer)