from datetime import date
from pydantic import BaseModel, Field, model_validator


class DateRange(BaseModel):
    start: date
    end: date

    @model_validator(mode="after")
    def valid_range(self):
        if self.end < self.start:
            raise ValueError("end must be on or after start")
        if (self.end - self.start).days > 366:
            raise ValueError("date range cannot exceed 366 days")
        return self


class ChatRequest(BaseModel):
    message: str = Field(min_length=3, max_length=500)


class ReminderRequest(BaseModel):
    order_id: int


class CreateOrderRequest(BaseModel):
    customer_email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    total_paise: int = Field(gt=0, le=10_000_000)


class CaptureRequest(BaseModel):
    order_id: int
    paypal_order_id: str = Field(min_length=5, max_length=128)
