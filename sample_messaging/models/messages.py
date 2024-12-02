from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

# Define the Recipient model
class Recipient(BaseModel):
    name: str
    phone: str
    id: str


# Define the Message model
class Message(BaseModel):
    from_: str = Field(alias="from") # Use "form_" becase "from" is a reserved keyword in python
    content: str
    id: str
    status: str
    createdAt: datetime
    deliveredAt: Optional[datetime]
    to: Union[Recipient, str]


# Define the PaginatedMessagesResponse model
class PaginatedMessagesResponse(BaseModel):
    messages: List[Message]
    page: str
    quantityPerPage: str
