PySMSCenter is a developing Python library designed to facilitate the sending and managing of SMS messages via the `smscenter.gr` API. Currently, it supports basic functionalities such as sending SMS, checking account balances, and validating mobile numbers, with plans to extend features.

## Features

- **Mobile Number Validation**: Check the validity of mobile numbers.
- **SMS Sending**: Easily send SMS messages to one or multiple recipients.
- **Balance Management**: Check and manage your SMS account balance. -
- **SMS History**: Retrieve and view your SMS sending history.
- **Status Checks**: Monitor the delivery status of your messages.
- **Contact Management**: Manage your contact list for easier SMS operations.

## Planed Features

- **Viber Management**
- **Group Management**

## Getting Started

### Prerequisites

- Python 3.11
- An API key from [smscenter](https://smscenter.gr/api/docs/en?ModPagespeed=off#how-to-start)

### Installation

Currently, the library is available directly from the source. Clone or download the repository from GitHub, then install requirements using pip.

### Send Single SMS

```python
from smsclient import SMSClient

client = SMSClient("api_key")

send_single_sms = client.sms.send(to="1234567890", text="Hello World", sender="Test")
```

### Send Batch

```python
mobile_numbers = ["1234567890","2234567890","3234567890"]
client.sms.bulk(to=mobile_numbers, text="Hello World", sender="Test")
```

### SMS Balance

```python
client.balance.check()
```

### SMS History

```python
client.history.single_list()
```

### Check Mobile

```python
client.mobile.check(mobile="1234567890")
```

### SMS Status

```python
client.status.sms(sms_id="123456")
```

### Contacts

```python
contact_list = client.contact.list()

# add contact
client.contact.add(
	mobile="1234567890",
	name="John",
	surname="Doe"
)

# Get contact
client.contact.get(contact_id="123456")

# Delete a contact
client.contact.delete(contact_id="123456")

```

### You can find the api documentation from [smscenter.gr](https://smscenter.gr/api/docs/en?ModPagespeed=off)

## Contributing

We welcome contributions to help grow and improve this library. Please refer to our contributing guidelines for more information on how to submit issues, fixes, or enhancements..
