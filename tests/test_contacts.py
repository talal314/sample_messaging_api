import unittest
from unittest.mock import patch
from pydantic import ValidationError
from requests import HTTPError

from sample_messaging.api.contacts import ContactsClient
from sample_messaging.models.contacts import Contact, PaginatedContactsResponse

class TestContactsClient(unittest.TestCase):
    def setUp(self):
        self.contacts_clinet = ContactsClient()

    @patch('sample_messaging.client.Client.handle_request')
    def test_get_contacts_success(self, mock_handle_request):
        mock_handle_request.return_value = {
            'contacts': [
                {'id': '1', 'name': 'test name 1', 'phone': '+123456789'},
                {'id': '2', 'name': 'test name 2', 'phone': '+123456789'}
            ],
            'pageNumber': 1,
            'pageSize': 10
        }

        response = self.contacts_clinet.get_contacts(page_index=1, max_items=10)

        # Assertions
        self.assertIsInstance(response, PaginatedContactsResponse)
        self.assertEqual(len(response.contacts), 2)
        self.assertEqual(response.contacts[0].name, 'test name 1')


    @patch('sample_messaging.client.Client.handle_request')
    def test_get_contacts_validation_error(self, mock_handle_request):
        mock_handle_request.return_value = {
            'contacts': [
                {'id': '1', 'name': 'test name 1', 'phone': '+123456789'},
                {'id': '2', 'name': 'test name 2', 'phone': '+123456789'}
            ],
            'pageNumber': 'string-number',
            'pageSize': 10
        }

        with self.assertRaises(ValidationError):
            self.contacts_clinet.get_contacts(page_index=1, max_items=10)


    @patch('sample_messaging.client.Client.handle_request')
    def test_create_contact_success(self, mock_handle_request):
        mock_handle_request.return_value = {'id': '3', 'name': 'test name 1', 'phone': '+123456789'}

        response = self.contacts_clinet.create_contact(name='test name 1', phone='+123456789')

        # Assertions
        self.assertIsInstance(response, Contact)
        self.assertEqual(response.name, 'test name 1')


    @patch('sample_messaging.client.Client.handle_request')
    def test_get_contact_success(self, mock_handle_request):
        mock_handle_request.return_value = {'id': '3', 'name': 'test name 1', 'phone': '+123456789'}

        response = self.contacts_clinet.get_contact(id='1')

        # Assertions
        self.assertIsInstance(response, Contact)
        self.assertEqual(response.name, 'test name 1')


    @patch('sample_messaging.client.Client.handle_request')
    def test_update_contact_success(self, mock_handle_request):
        mock_handle_request.return_value = {'id': '3', 'name': 'Updated name', 'phone': '+123456789'}

        response = self.contacts_clinet.update_contact(id='1', new_name='Updated name', new_phone='+1111111111')

        # Assertions
        self.assertIsInstance(response, Contact)
        self.assertEqual(response.name, 'Updated name')


    @patch('sample_messaging.client.Client.handle_request')
    def test_update_contacts_http_error(self, mock_handle_request):
        mock_handle_request.side_effect = HTTPError("404 Not found")

        with self.assertRaises(HTTPError):
            self.contacts_clinet.update_contact(id='1', new_name='Updated name', new_phone='+1111111111')


    @patch('sample_messaging.client.Client.handle_request')
    def test_delete_contact_success(self, mock_handle_request):
        mock_handle_request.return_value = None

        response = self.contacts_clinet.delete_contact(id='1')

        # Assertions
        self.assertIsNone(response)
