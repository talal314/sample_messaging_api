from pydantic import BaseModel
from typing import List

# Define the Contact model
class Contact(BaseModel):
    id: str
    name: str
    phone: str


# Define the Pagination model
class Pagination(BaseModel):
    page_number: int
    page_size: int


# Define the PaginatedContactsResponse model
class PaginatedContactsResponse(BaseModel):
    contacts: List[Contact]
    pagination: Pagination
