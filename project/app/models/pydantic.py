from typing_extensions import Self
from pydantic import BaseModel, model_validator, Field

class SendSmsPayloadSchema(BaseModel):
    name: str
    phone_number: str = Field(
        max_length=12,
        description="Phone number should not be longer than 12 characters"
    )

    @model_validator(mode="after")
    def validate_phone_number(self) -> Self:  
        if self.phone_number.startswith("07") and len(self.phone_number) == 10:
            self.phone_number = f"2547{self.phone_number[3:]}"
        return self