# fake.legal Python SDK & CLI

Official Python client and CLI tool for the [fake.legal](https://fake.legal) Temporary Email API. No dependencies required.

## Installation

Simply download `fake_legal.py` and place it in your project directory.

Or install it directly from GitHub:
```bash
pip install git+https://github.com/LeqitLama/fake-legal-python.git
```

## CLI Usage

Generate a random temporary email address:
```bash
fake-legal generate
```

Generate a random email address with a specific domain:
```bash
fake-legal generate --domain imgui.de
```

Create a custom email address:
```bash
fake-legal custom myusername fake.legal
```

Check the inbox for a specific address:
```bash
fake-legal inbox myusername@fake.legal
```

Fetch the full content of a specific email by its ID:
```bash
fake-legal email abc-123
```

### Premium API Keys
If you purchased a Premium API key to bypass rate limits, pass it with the `--api-key` option:
```bash
fake-legal --api-key USER_A1B2C3 generate
```

## Python SDK Usage

```python
from fake_legal import FakeLegal

# Initialize client (Free Tier)
client = FakeLegal()

# Initialize client with Premium Key
# client = FakeLegal(api_key="USER_A1B2C3")

# Create a random inbox
inbox = client.create_inbox()
email_address = inbox["address"]
print(f"Generated: {email_address}")

# Create a custom inbox
custom = client.create_custom_inbox("devtest", "fake.legal")

# Fetch emails
messages = client.get_emails(email_address)
if messages.get("exists") and messages.get("emails"):
    for msg in messages["emails"]:
        print(f"[{msg['id']}] From: {msg['from']} - Subject: {msg['subject']}")
        
        # Read full content
        full_email = client.get_email(msg['id'])
        print(full_email["email"]["text"])
```

## License
MIT
