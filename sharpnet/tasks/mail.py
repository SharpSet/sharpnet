import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sharpnet.constants import HTMLFILE

sender_email = "mcadesignsmail@gmail.com"
receiver_email = "adam@mcaq.me"
password = os.environ.get("MAILPASS")

def mail_error(self, container):

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Error in Container {container.name}"
    message["From"] = sender_email
    message["To"] = receiver_email

    with open(HTMLFILE) as html:
        html = html.read()

    text = f"""
        There was an unexpected error in container {container.name}. <br><br> Is has been killed by the Sharpnet Instance. If you are running SharpCD, click the link below to be taken directly to the logs.
    """

    html = html.replace("XXXXX", text)

    # Turn these into plain/html MIMEText objects
    main = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(main)

    # Create secure connection with server and send email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )