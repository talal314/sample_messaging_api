# sample_messaging_api
Developer Experience Assessment for sinch interview

## How to use?

There are several steps you should follow in order to use the SDK.  

### Create virtual environment

Create new python enviornment using these commands:

```
python3 -m venv myenv
source myenv/bin/activate
```

### Install the SDK.

You can install the sdk using this command after moving to SDK directory

```
pip install .
```

Also you should install flask in order to use the webhooks server

```
pip install flask
```

Test that the SDK was installed correctly using this command

```
python3 -c "import sample_messaging; print('Sample Messaging imported successfully')"
```

### Run Python commands to communicate with the API

Let's test the API related with the contacts, for example create a new contact. In order to do it, we need to run this command:

```
python3 -c "from sample_messaging.api.contacts import ContactsClient; print(ContactsClient().create_contact(name='Test', phone='+3411111111'))"
```

We will get a response showing the id, name and the phone number of the contact.

In the same way, we can test all the other methods related to the contacts and messages.

### Run the tests

We can run the tests using this command:
```
python3 -m unittest discover -v
```

### Webhooks tasks

In order to recieve a webhooks, first of all we need to change the webhooks URL to this one 'http://172.17.0.1:3010/webhooks', to enable the connection between the docker container and the host.

After that we run our flask server using these commands:
```
cd webhook-server/
python3 app.py
```

We get the conacts to get the id from it:

```
python3 -c "from sample_messaging.api.contacts import ContactsClient; print(ContactsClient().get_contacts())"
```

Choose an id and use it to create a new message:
```
python3 -c "from sample_messaging.api.messages import MessagesClient; print(MessagesClient().create_message('test@gmail.com', 'Test content', {id}))"
```

You will receive in our webhooks server 200 ok response indicating that everything is working fine
```
Valid signature...
172.20.0.4 - - [03/Dec/2024 11:36:25] "POST /webhooks HTTP/1.1" 200 -
```
