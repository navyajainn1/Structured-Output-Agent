from agent import get_validated_response


response = get_validated_response(
    "I have chest pain and want to see a doctor."
)

print("\nFINAL RESPONSE:")
print(response)