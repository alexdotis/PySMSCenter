# PySMSClient

PySMSClient is a comprehensive Python library designed to facilitate the sending and managing of SMS messages via the `smscenter.gr` API. It offers robust session management and error handling to ensure reliability and efficiency for various SMS-related operations.

## Features

- **Mobile Number Validation**: Check the validity of mobile numbers.
- **SMS Sending**: Easily send SMS messages to one or multiple recipients.
- **Balance Management**: Check and manage your SMS account balance.
- **SMS History**: Retrieve and view your SMS sending history.
- **Status Checks**: Monitor the delivery status of your messages.
- **Contact Management**: Manage your contact list for easier SMS operations.


## Usage
```python
from smsclient import SMSClient

client = SMSClient("api_key")

mobile = client.mobile.check("0123456789") # mobile phone

sms_send = client.sms.send(to="test_mobile", text="Hello World", sender="Test")
```

### You can find the api documentation from [smscenter.gr](https://smscenter.gr/api/docs/en?ModPagespeed=off)
