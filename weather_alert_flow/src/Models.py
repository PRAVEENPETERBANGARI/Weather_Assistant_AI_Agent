from pydantic import BaseModel, Field

class WeatherGuardrailOutput(BaseModel):
    place_name: list[str] = Field(description="List of place names relevant to the weather guardrail output")
    is_place_specified: bool = Field(description="Indicates if a place was specified in the input")

class MailComponents(BaseModel):
    subject: str = Field(description="Subject line of the email")
    html_body: str = Field(description="HTML content of the email body")