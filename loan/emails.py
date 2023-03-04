from django.template.loader import render_to_string
from mailjet_rest import Client
import os

api_key = '54cc70751de8566f41113b002c40e827'
api_secret = '86815b74241ecc1eaad34f9237f69057'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_email(message, to, name, subject):
    email_body = message
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "dorothyvic24@gmail.com",
                    "Name": "Quick loans"
                },
                "To": [
                    {
                        "Email": to,
                        "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": "Accsol",
                "HTMLPart": email_body,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
