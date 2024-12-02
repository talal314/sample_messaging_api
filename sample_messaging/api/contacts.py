import requests
from pydantic import ValidationError

from ..client import Client
from ..constants import API_KEY, BASE_URL
from ..models.contacts import Contact, PaginatedContactsResponse


class ContactsClient:

    def __init__(self):
        self.client = Client(base_url=BASE_URL, api_key=API_KEY)


    def get_contacts(self, page_index=0, max_items=10):
        """
        Fetches a list of contacts from the API.

        Args:
            page_index: Optional, by default 0
            max_items:  Optional, by default 10
        
        Returns:
            a list of Contact objects ('contacts') with the pagination parameters
        """
        try:
            params = {
                'pageIndex': page_index,
                'max': max_items
            }
            response = self.client.handle_request("GET", "contacts", params)
            paginated_response = PaginatedContactsResponse(
                contacts=response['contacts'],
                pagination={
                    'page_number': response['pageNumber'],
                    'page_size': response['pageSize']
                }
            )
            return paginated_response

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise


    def create_contact(self, name:str, phone: str):
        """
        Create new contact in the API

        Args:
            name: Contact name
            phone: Contact phone number
        
        Returns:
            created contact object.
        """
        try:
            data = {
                'name': name,
                'phone': phone
            }
            response = self.client.handle_request("POST", "contacts", data=data)
            return Contact(**response)

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise


    def get_contact(self, id: str):
        """
        Fetches a contact from the API

        Args:
           id: Contact id

        Returns:
           contact object .
        """
        try:
            response = self.client.handle_request("GET", f"contacts/{id}")
            return Contact(**response)

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise


    def update_contact(self, id: str, new_name: str, new_phone: str):
        """
        Update a contact in the API.

        Args:
            id: contact id
            new_name: new contact name
            new_phone: new contact phone number

        Returns:
            updated contact object.
        """
        try:
            data = {
                'name': new_name,
                'phone': new_phone
            }
            
            response = self.client.handle_request("PATCH", f"contacts/{id}", data=data)
            return Contact(**response)

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise


    def delete_contact(self, id: str):
        """
        Delete one contact from the API.

        Args:
            id: contact id

        Returns: 
            None, no content.
        """
        try:
            return self.client.handle_request("DELETE", f"contacts/{id}")

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise
