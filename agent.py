import os
from dotenv import load_dotenv
from groq import Groq
from schemas import ClinicResponse
from logger import log_validation_failure

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def call_llm(user_message: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You are a clinic chatbot.

Return ONLY valid JSON.

The JSON MUST follow this exact structure:

{
    "message": "string",
    "urgent": true or false,
    "nextSteps": ["string"],
    "contactInfo": {
        "clinicPhone": "string",
        "emergencyPhone": "string",
        "urgentCare": "string"
    },
    "symptomCheck": "string",
    "timestamp": "string"
}

Do not use markdown.
Do not add any fields.
Do not remove any required fields.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def get_validated_response(user_message: str, max_retries: int = 3):

    validation_error = None

    for attempt in range(1, max_retries + 1):

        print(f"\nAttempt {attempt}/{max_retries}")

        if validation_error:

            retry_message = f"""
Your previous response failed Pydantic validation.

Validation error:
{validation_error}

You MUST fix these errors and return the complete JSON response.

Return ONLY JSON.
Do not use markdown.
Do not add explanations.
"""

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a clinic chatbot.

Return ONLY valid JSON.

The response MUST contain:

{
    "message": "string",
    "urgent": true or false,
    "nextSteps": ["string"],
    "contactInfo": {
        "clinicPhone": "string",
        "emergencyPhone": "string",
        "urgentCare": "string"
    },
    "symptomCheck": "string",
    "timestamp": "string"
}

Do not use markdown.
Do not add explanations.
"""
                    },
                    {
                        "role": "user",
                        "content": user_message
                    },
                    {
                        "role": "user",
                        "content": retry_message
                    }
                ],
                temperature=0
            )

            raw_response = response.choices[0].message.content

        else:

            raw_response = call_llm(user_message)

        try:

            validated_response = ClinicResponse.model_validate_json(
                raw_response
            )

            print("Validation successful!")

            return validated_response

        except Exception as error:

            validation_error = str(error)

            print("Validation failed!")
            print(validation_error)

            log_validation_failure(
                attempt,
                validation_error
            )

    raise ValueError(
        f"LLM failed validation after {max_retries} attempts."
    )