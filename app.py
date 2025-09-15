import asyncio
from email.message import EmailMessage
from aiosmtpd.controller import Controller
import smtplib
from flask import Flask

SMTP_HOST = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USER = "970951001@smtp-brevo.com"
SMTP_PASS = "kpF2B0N1sLKGVUtW"

FROM = "yourverified@customdomain.com"
TO = "jaiprataps830@gmail.com"

# SMTP forwarder handler
class ForwardHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Received email from:", envelope.mail_from)
        print("To:", envelope.rcpt_tos)
        print("Content:", envelope.content.decode(errors='ignore'))

        # Forward to Gmail / Yahoo via Brevo SMTP
        msg = EmailMessage()
        msg.set_content(envelope.content.decode(errors='ignore'))
        msg['Subject'] = "Forwarded message"
        msg['From'] = FROM
        msg['To'] = TO

        # send via Brevo
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
            print("Forwarded message sent.")

        return '250 Message accepted for delivery'

app = Flask(__name__)

@app.route("/")
def index():
    return "Running"

if __name__ == "__main__":
    controller = Controller(handler=ForwardHandler(), hostname='0.0.0.0', port=2525)
    controller.start()

    app.run(host="0.0.0.0", port=3000)
