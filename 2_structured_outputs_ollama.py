import ollama
from pydantic import BaseModel


# ------------------------------------------------
# 1. Define the expected structure
# ------------------------------------------------

class Person(BaseModel):
    name: str
    age: int
    city: str


# ------------------------------------------------
# 2. Structured output with Pydantic + Ollama
# ------------------------------------------------

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Give me the name, age and city of a fictional person."
        }
    ],
    format=Person.model_json_schema(),
    options={
        "temperature": 0
    }
)


# ------------------------------------------------
# 3. Get the raw response
# ------------------------------------------------

# print("Raw response:")
# print(response["message"]["content"])


# ------------------------------------------------
# 4. Validate and convert to Pydantic object
# ------------------------------------------------

person = Person.model_validate_json(
    response["message"]["content"]
)


# ------------------------------------------------
# 5. Access individual fields
# ------------------------------------------------

print("\nPydantic object:")
print(person)

print("\nIndividual fields:")
print(person.name)
print(person.age)
print(person.city)