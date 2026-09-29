from pydantic import BaseModel
from typing import Literal


class ContactInfo(BaseModel):
    clinicPhone: str
    emergencyPhone: str
    urgentCare: str


class ClinicResponse(BaseModel):
    message: str
    urgent: bool
    nextSteps: list[str]
    contactInfo: ContactInfo
    symptomCheck: str
    timestamp: str