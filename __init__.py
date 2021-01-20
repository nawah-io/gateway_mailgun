# Ancora Imparo.

from nawah.classes import PACKAGE_CONFIG, ATTR
from nawah.registry import Registry

from typing import Dict, Any, TypedDict
import requests, json


def mailgun_messages_gateway(
	subject: str,
	addr_to: str,
	content: str = None,
	template: str = None,
	data: Dict[str, Any] = None,
	sender: str = None,
	mailgun_auth: TypedDict(
		'GATEWAY_MAILGUN_MESSAGES_AUTH', key=str, uri=str, sender_name=str, sender_email=str
	) = None,
):
	if (not content and not template) or (content and template):
		raise Exception(
			'Either \'content\' or \'template\' should be passed when using Gateway \'mailgun_messages\'.'
		)

	if (not sender and not mailgun_auth) or (sender and mailgun_auth):
		raise Exception(
			'Either \'sender\' or \'mailgun_auth\' should be passed when using Gateway \'mailgun_messages\'.'
		)

	if not mailgun_auth:
		mailgun_auth = Registry.var('mailgun')
		mailgun_auth = {
			'key': mailgun_auth['key'],
			'uri': mailgun_auth['senders'][sender]['uri'],
			'sender_name': mailgun_auth['senders'][sender]['sender_name'],
			'sender_email': mailgun_auth['senders'][sender]['sender_email'],
		}

	request_data = {
		'from': f'{mailgun_auth["sender_name"]} <{mailgun_auth["sender_email"]}>',
		'to': [addr_to],
		'subject': subject,
	}

	if content:
		request_data['text'] = content
	else:
		request_data['template'] = template

	if data:
		request_data['h:X-Mailgun-Variables'] = json.dumps(data)

	request = requests.post(
		mailgun_auth['uri'],
		auth=('api', mailgun_auth['key']),
		data=request_data,
	)

	if request.status_code != 200:
		raise Exception(
			f'Failed to send \'messages\' request with Mailgun API response: {request.text()}'
		)


def mailgun_newsletters_gateway(
	subscribed: bool,
	address: str,
	name: str,
	description: str,
	newsletter: str = None,
	mailgun_auth: TypedDict('GATEWAY_MAILGUN_NEWSLETTERS_AUTH', key=str, uri=str) = None,
):
	if newsletter and mailgun_auth:
		raise Exception(
			'Either \'newsletter\' or \'mailgun_auth\' should be passed when using Gateway \'mailgun_newsletters\'.'
		)

	if not mailgun_auth:
		mailgun_auth = Registry.var('mailgun')
		mailgun_auth = {
			'key': mailgun_auth['key'],
			'uri': mailgun_auth['newsletters'][newsletter],
		}

	request = requests.post(
		mailgun_auth['uri'],
		auth=('api', mailgun_auth['key']),
		data={
			'subscribed': subscribed,
			'address': address,
			'name': name,
			'description': description,
		},
	)

	if request.status_code != 200:
		raise Exception(
			f'Failed to send \'newsletters\' request with Mailgun API response: {request.text()}'
		)


config = PACKAGE_CONFIG(
	api_level='1.1',
	version='1.1.0b1',
	gateways={
		'mailgun_messages': mailgun_messages_gateway,
		'mailgun_newsletters': mailgun_newsletters_gateway,
	},
	vars_types={
		'mailgun': ATTR.TYPED_DICT(
			dict={
				'key': ATTR.STR(),
				'newsletters': ATTR.KV_DICT(key=ATTR.STR(), val=ATTR.STR()),
				'senders': ATTR.KV_DICT(
					key=ATTR.STR(),
					val=ATTR.TYPED_DICT(
						dict={
							'uri': ATTR.URI_WEB(allowed_domains=['api.mailgun.net'], strict=True),
							'sender_name': ATTR.STR(),
							'sender_email': ATTR.EMAIL(),
						}
					),
				),
			}
		)
	},
)
