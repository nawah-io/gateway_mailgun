# Nawah Gateway for Mailgun
This repo is a [Nawah](https://github.com/nawah-io/nawah_docs) Package that allows developers to integrate [Mailgun](https://www.mailgun.com) into Nawah apps using Gateway Controller. This packages offers two gateways; `mailgun_messages` which allows developers to send messages with Mailgun REST API, and `mailgun_newsletters` which allows developers to manage Mailgun newsletters subscriptions using Mailgun REST API.

## How-to
1. From your app directory run: `nawah packages add gateway_mailgun`
2. Add `mailgun` Var to `nawah_app.py` App Config:
```python
vars = {
	'mailgun': {
        'key': 'MAILGUN_API_KEY',
        'newsletters': {
            # If you are not using this gateway to manage newsletters keep newsletters present but empty
            'NEWSLETTER_ID': 'NEWSLETTER_REST_URI',
        },
        'senders': {
            # If you are not using this gateway to send messages keep senders present but empty
            'SENDER_ID': {
                'uri': 'SENDER_REST_URI',
                'sender_name': 'NAME_OF_SENDER',
                'sender_email': 'EMAIL_ADDRESS_OF_SENDER',
            }
        },
   }
}
```
3. `mailgun_messages` gateway requires following arguments:
   1. `subject`: Subject of the message being sent. Type `str`.
   2. `addr_to`: Email address the message is being sent to. Type `str`.
   4. `content` or `template`: One of these two arguments should be present:
      1. `content`: Literal message content to be sent. Type `str`.
      2. `template`: Template name registered in Mailgun to be used for this message. Type `str`.
   5. `data`: When sending message with `template` you can pass set of values to replace Mailgun template variables with. Type `dict`.
   6. `sender` or `mailgun_auth`: One of these two arguments should be present:
      1. `sender`: Sender identifier from one of `mailgun.senders`. Type `str`.
      2. `mailgun_auth`: Value used to pass dynamic API credentials with following values (Type `dict`):
         1. `key`: Mailgun API key to be used. Type `str`.
         2. `uri`: Mailgun REST API URI for message sending request. Type `str`.
         3. `sender_name`: Name of the sender to be present on message. Type `str`.
         4. `sender_email`: Sender email address to be present on message. Type `str`.
4. Use `mailgun_messages` using Nawah Gateway Controller:
```python
from nawah.gateway import Gateway

Gateway.send(gateway='mailgun_messages', subject=subject, addr_to=addr_to, content=content, sender=sender)
Gateway.send(gateway='mailgun_messages', subject=subject, addr_to=addr_to, template=template, data=data, sender=sender)
Gateway.send(gateway='mailgun_messages', subject=subject, addr_to=addr_to, content=content, mailgun_auth=mailgun_auth)
```
5. `mailgun_newsletters` gateway requires following arguments:
   1. `subscribed`: Boolean value stating whether the email address is subscribed to newsletter or not. Type `bool`.
   2. `address`: Email address to be added to newsletter. Type `str`.
   3. `name`: Name of the email address owner. Type `str`.
   4. `description`: Description of the request begin sent, for internal uses. Type `str`.
   6. `newsletter` or `mailgun_auth`: One of these two arguments should be present:
      1. `newsletter`: Newsletter identifier from one of `mailgun.newsletters`. Type `str`.
      2. `mailgun_auth`: Value used to pass dynamic API credentials with following values (Type `dict`):
         1. `key`: Mailgun API key to be used. Type `str`.
         2. `uri`: Mailgun REST API URI for newsletter request. Type `str`.
6. Use `mailgun_newsletters` using Nawah Gateway Controller:
```python
from nawah.gateway import Gateway

Gateway.send(gateway='mailgun_newsletters', subscribed=subscribed, address=address, name=name, description=description, newsletter=newsletter)
Gateway.send(gateway='mailgun_newsletters', subscribed=subscribed, address=address, name=name, description=description, mailgun_auth=mailgun_auth)
```