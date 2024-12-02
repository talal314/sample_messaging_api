import requests
from pydantic import ValidationError

from ..client import Client
from ..constants import API_KEY, BASE_URL
from ..models.messages import Message, PaginatedMessagesResponse


class MessagesClient:

    def __init__(self):
        self.client = Client(base_url=BASE_URL, api_key=API_KEY)


    def get_messages(self, page_index=0, max_items=10):
        """
        Fetches a list of messages from the API.

        Args:
            page_index: Optional, by default 0
            max_items: Optional, by default 10
        
        Returns:
            a list of Message objects ('messages') with the pagination parameters
        """
        try:
            params = {
                'page': page_index,
                'limit': max_items
            }
            response = self.client.handle_request("GET", "messages", params=params)

            paginated_response = PaginatedMessagesResponse(
                messages = response['messages'],
                page = response['page'],
                quantityPerPage = response['quantityPerPage']
            )
            return paginated_response

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise
  

    def create_message(self, from_: str, content: str, id: str):
        """
        Create new message in the API.

        Args:
            from_: Identify the message where is coming from 
            content: message content
            id: contact id

        Returns:
            created message object
        """
        try:
            data = {
                'from': from_,
                'content': content,
                'to': {
                    'id': id
                }
            }
            response = self.client.handle_request("POST", "messages", data=data)
            return Message(**response)

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise


    def get_message(self, id: str):
        """
        Fetches a message from the API

        Args:
            id: message id
        
        Returns: 
            Message object
        """
        try:
            response = self.client.handle_request("GET", f"messages/{id}")
            return Message(**response)

        except ValidationError as e:
            raise
        except requests.HTTPError as http_err:
            raise
