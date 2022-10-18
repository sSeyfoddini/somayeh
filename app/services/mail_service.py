import boto3
from botocore.exceptions import ClientError

from app.config import Config


class MailService:
    @classmethod
    def send_mail(self, first_name, last_name, otp, reciever):
        SENDER = Config.SENDER
        RECIPIENT = reciever
        AWS_REGION = Config.REGION

        SUBJECT = f"Pocket Verification Code for {first_name} {last_name}"

        BODY_HTML = f"""<html>
       <div style=" margin:24px; width:800px">
        <a href="https://www.getpocket.io/"><img src="https://dev.getpocket.io/console/assets/images/pocket_logo_name.png" width=300px /></a>
        <p style="font-family:Tahoma, Verdana, sans-serif">Hi {first_name} {last_name}!</p>
        <p style="font-family:Tahoma, Verdana, sans-serif">We have received a request to create your Pocket&trade; account. As a security precaution, you'll need to enter the following code into the Pocket app to complete activation:</p>
        <p style="padding: 32px;text-align: center; font-family:Tahoma, Verdana, sans-serif; display: inline-block; background-color:#5B01AA; color:white;padding:6px 12px;text-decoration:none">{otp}</p>
        <p style="font-family:Tahoma, Verdana, sans-serif">If you did not install the Pocket App, someone has tried to create a Pocket account using your email address.</p>
        <p style="font-family:Tahoma, Verdana, sans-serif">Thanks!</p>
        <p style="font-family:Tahoma, Verdana, sans-serif">The Pocket Team</p>
        </html> 
            """

        CHARSET = "UTF-8"
        client = boto3.client("ses", region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                        RECIPIENT,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": CHARSET,
                            "Data": BODY_HTML,
                        }
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
