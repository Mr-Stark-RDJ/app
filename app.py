from flask import Flask, request
import smtpd
import asyncore
import threading
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# SMTP server (for receiving emails)
class ForwardingSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("Received message from:", peer)
        print("From:", mailfrom)
        print("To:", rcpttos)
        print("Data:", data)
        # Optionally forward to Gmail/Yahoo
        try:
            msg = EmailMessage()
            msg.set_content(data)
            msg['Subject'] = "Forwarded: " + (mailfrom or "")
            msg['From'] = "your@customdomain.com"
            msg['To'] = "yourgmail@gmail.com"
            
            # Use trusted SMTP (e.g. Brevo) to send
            smtp_host = "smtp-relay.brevo.com"
            smtp_port = 587
            smtp_user = "your-brevo-smtp-user"
            smtp_pass = "your-brevo-smtp-pass"
            
            with smtplib.SMTP(smtp_host, smtp_port) as s:
                s.starttls()
                s.login(smtp_user, smtp_pass)
                s.send_message(msg)
            print("Forwarded message to Gmail.")
        except Exception as e:
            print("Error forwarding:", e)
        return

def run_smtp_server():
    server = ForwardingSMTPServer(("0.0.0.0", 2525), None)
    try:
        asyncore.loop()
    except Exception as e:
        print("SMTP server stopped:", e)

@app.route("/")
def index():
    return "Hello from Railway SMTP app"

if __name__ == "__main__":
    # start the smtp server in background thread
    t = threading.Thread(target=run_smtp_server, daemon=True)
    t.start()
    # start flask
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", "3000")))
