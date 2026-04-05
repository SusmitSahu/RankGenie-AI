from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID="XXXXXXXXXXXXXXXX"
TWILIO_AUTH_TOKEN="XXXXXXXXXXXXXXXX"
TWILIO_PHONE=+123456789
ALERT_PHONE="(Your Device number)"


def send_sms_alerts(alerts):

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    from_phone = os.getenv("TWILIO_PHONE")
    to_phone = os.getenv("ALERT_PHONE")

    client = Client(account_sid, auth_token)

    message_body = "🚨 Top Infrastructure Alerts\n\n"

    for a in alerts:

        message_body += (
            f"ID: {a['id']}\n"
            f"Severity: {a['severity']}\n"
            f"Priority: {round(a['priority_score'],2)}\n"
            f"Status: {a['status']}\n"
            f"----\n"
        )

    client.messages.create(
        body=message_body,
        from_=from_phone,
        to=to_phone
    )