# PySMSCenter

Python SMS SDK for SMSCenter API integration.

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-success)

> **Unofficial** Python SDK for smscenter.gr - not affiliated with or endorsed by SMSCenter.

PySMSCenter is a modern, typed Python SDK for integrating with the SMSCenter REST API.  
It allows developers to send SMS messages, manage contacts and groups, perform HLR lookups, handle bulk SMS campaigns and implement two-factor authentication (2FA) workflows in Python applications.

`pysmscenter` provides a structured, well-tested interface for sending and managing SMS messages via [smscenter](https://smscenter.gr/api/docs/en?ModPagespeed=off#how-to-start)

## ✨ Features

- 📱 Send Single SMS
- 📤 Send Bulk SMS
- 📊 Check Account Balance
- 📖 SMS History (Single & Grouped)
- 📬 Delivery Status Tracking
- 👤 Contact Management
- 👥 Group Management
- 🔐 Two-Factor Authentication (2FA)
- 🔎 HLR Lookup
- 👥 Sub-account Management
- 🔁 Automatic Retry Support
- ⚠️ Domain-Specific Exceptions
- 🧪 Fully Tested
- 🐍 Python 3.12+

---

## Planned Features

- **Viber Management**

## 📦 Installation

Once published to PyPI:

```bash
pip install pysmscenter
```

Until then:

```bash
git clone https://github.com/yourusername/PySMSCenter.git
cd PySMSCenter
pip install .
```

## 🔐 Authentication

You need an API key from:

https://smscenter.gr/api/docs/en

### Using API Key

```python
from pysmscenter import SMSClient

client = SMSClient("your_api_key")
```

### Using Username & Password

```python
from pysmscenter import SMSClient

client = SMSClient.from_credentials("username", "password")
```

---

## 🚀 Basic Usage

### Context Manager (Recommended)

```python
from pysmscenter import SMSClient

with SMSClient("your_api_key") as client:
    balance = client.balance.check()
    print(balance.get("balance"))
```

---

## 📱 SMS

## Send Single SMS

```python
client.sms.send(
    to="306912345678",
    text="Hello World",
    sender="MyApp"
)
```

## Send Bulk SMS

```python
numbers = ["306912345678", "306912345679"]

client.sms.bulk(
    to=numbers,
    text="Bulk message",
    sender="MyApp"
)
```

## Cancel Scheduled SMS

```python
client.sms.cancel("sms_id_here")
```

## 📊 Account & Status

## Check Balance

```python
client.balance.check()
```

## Check Delivery Status

```python
client.status.sms("sms_id_here")
```

## Get Recent Status Reports

```python
client.status.get()
```

---

## 📖 History

## Single SMS History

```python
client.history.single_list()
```

## Grouped SMS History

```python
client.history.group_list()
```

---

## 👤 Contacts

## List Contacts

```python
client.contact.list()
```

## Add Contact

```python
client.contact.add(
    mobile="306912345678",
    name="John",
    surname="Doe",
)
```

## Update Contact

```python
client.contact.update(
    contact_id="12345",
    name="Updated Name"
)
```

## Delete Contact

```python
client.contact.delete("12345")
```

---

## 👥 Groups

## Create Group

```python
client.group.add("Customers")
```

## Add Contact to Group

```python
client.group.add_contact(
    group_id="123",
    contact_id="456"
)
```

## Remove Contact from Group

```python
client.group.delete_contact(
    group_id="123",
    contact_id="456"
)
```

---

## 🔎 Mobile & HLR

## Validate Mobile Number

```python
client.mobile.check("306912345678")
```

## HLR Lookup

```python
client.hlr.lookup("306912345678")
```

---

## 🔐 Two Factor Authentication

## Send 2FA Code

```python
response = client.two_factor.send(
    to="306912345678",
    text="Your verification code is %%code%%"
)
```

## Verify 2FA Code

```python
client.two_factor.check(
    auth_id="auth_id_from_send",
    code="1234"
)
```

---

## 👥 Sub-Accounts

## Create Sub-Account

```python
client.user.add(
    email="subaccount@example.com",
    password="securepassword"
)
```

## Top-up Sub-Account

```python
client.user.topup(
    user_id="12345",
    sms="10",
    cost="5"
)
```

---

## ⚠️ Error Handling

All API errors raise domain-specific exceptions:

```python
from pysmscenter.exceptions import SMSExceptionError

try:
    client.sms.send(...)
except SMSExceptionError as exc:
    print("Error code:", exc.code)
    print("Message:", exc.message)
```

Credential issues raise:

```python
from pysmscenter.exceptions import CredentialError
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions are welcome.  
Please open an issue or submit a pull request.

## Keywords

Python SMS SDK, SMS API client, Bulk SMS Python, SMS Gateway integration, SMSCenter API wrapper, SMS REST client, Two Factor Authentication API, HLR Lookup API, Python messaging library
