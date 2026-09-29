from schemas import ClinicResponse
from agent import call_llm


user_message = "I have chest pain and want to see a doctor."

raw_response = call_llm(user_message)

print("RAW LLM RESPONSE:")
print(raw_response)

print("\nVALIDATING RESPONSE...")

try:
    validated_response = ClinicResponse.model_validate_json(raw_response)

    print("\nVALIDATION SUCCESSFUL!")
    print(validated_response)

except Exception as e:
    print("\nVALIDATION FAILED!")
    print(e)