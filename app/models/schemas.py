"""
Pydantic models for API request/response schemas.
"""

from typing import Optional

from pydantic import BaseModel, Field


class TriggerRequest(BaseModel):
    """Request model for triggering the daily motivational email."""
    
    to_email: Optional[str] = Field(
        None,
        description="Optional recipient email address. If not provided, uses GIRLFRIEND_EMAIL from environment."
    )


class EmailResponse(BaseModel):
    """Response model for email sending endpoint."""
    
    status: str = Field(..., description="Status of the operation")
    sent_to: str = Field(..., description="Email address where the quote was sent")
    quote: str = Field(..., description="The generated motivational quote")

