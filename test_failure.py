from schemas import ClinicResponse
from logger import log_validation_failure


bad_response = """
{
    "message": "Your appointment has been booked.",
    "urgent": false
}
"""

print("Testing invalid response...")

try:
    ClinicResponse.model_validate_json(bad_response)

except Exception as error:
    print("\nValidation failed!")
    print(error)

    log_validation_failure(
        attempt=1,
        error=str(error)
    )

    print("\nValidation error logged successfully!")