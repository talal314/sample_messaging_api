import unittest
from unittest.mock import patch
from pydantic import ValidationError
from requests import HTTPError

from sample_messaging.api.messages import MessagesClient
from sample_messaging.models.messages import Message, PaginatedMessagesResponse


class TestMessagesClient(unittest.TestCase):
    def setUp(self):
        self.messages_client = MessagesClient()

    @patch('sample_messaging.client.Client.handle_request')
    def test_get_contacts_success(self, mock_handle_request):
        mock_handle_request.return_value = {
            'messages': [
                {
                    'from': 'Sender1',
                    'content': 'Message 1',
                    'id': '1',
                    'status': 'queued',
                    'createdAt': '2024-11-30T10:11:30.508Z',
                    'deliveredAt': None,
                    'to': {'name': 'John', 'phone': '+123456789', 'id': '101'}
                },
                {
                    'from': 'Sender2',
                    'content': 'Message 2',
                    'id': '2',
                    'status': 'sent',
                    'createdAt': '2024-11-30T11:11:30.508Z',
                    'deliveredAt': '2024-11-30T12:00:00.000Z',
                    'to': {'name': 'Jane', 'phone': '+987654321', 'id': '102'}
                }
            ],
            'page': '1',
            'quantityPerPage': '10'
        }

        response = self.messages_client.get_messages(page_index=1, max_items=10)

        # Assertions
        self.assertIsInstance(response, PaginatedMessagesResponse)
        self.assertEqual(len(response.messages), 2)
        self.assertEqual(response.messages[0].content, 'Message 1')


    @patch('sample_messaging.client.Client.handle_request')
    def test_get_messages_validation_error(self, mock_handle_request):
        mock_handle_request.return_value = {
            'messages': [{'from': 'Sender1', 'id': '1', 'content': None}],
            'page': 1,
            'quantityPerPage': 10
        }

        with self.assertRaises(ValidationError):
            self.messages_client.get_messages(page_index=1, max_items=10)


    @patch('sample_messaging.client.Client.handle_request')
    def test_create_message_success(self, mock_handle_request):
        mock_handle_request.return_value = {
            'from': 'Sender1',
            'content': 'New Message',
            'id': '3',
            'status': 'queued',
            'createdAt': '2024-11-30T13:11:30.508Z',
            'deliveredAt': None,
            'to': {'name': 'Recipient', 'phone': '+111222333', 'id': '201'}
        }


        response = self.messages_client.create_message(from_='Sender1', content='New Message', id='201')

        # Assertions
        self.assertIsInstance(response, Message)
        self.assertEqual(response.content, 'New Message')
        self.assertEqual(response.to.name, 'Recipient')


    @patch('sample_messaging.client.Client.handle_request')
    def test_get_message_success(self, mock_handle_request):
        mock_handle_request.return_value = {
            'from': 'Sender1',
            'content': 'New Message',
            'id': '3',
            'status': 'queued',
            'createdAt': '2024-11-30T13:11:30.508Z',
            'deliveredAt': None,
            'to': {'name': 'Recipient', 'phone': '+111222333', 'id': '201'}
        }


        response = self.messages_client.get_message(id='3')

        # Assertions
        self.assertIsInstance(response, Message)
        self.assertEqual(response.content, 'New Message')


    @patch('sample_messaging.client.Client.handle_request')
    def test_get_message_http_error(self, mock_handle_request):
        mock_handle_request.side_effect = HTTPError("404 Not found")

        with self.assertRaises(HTTPError):
            self.messages_client.get_message(id='1')
