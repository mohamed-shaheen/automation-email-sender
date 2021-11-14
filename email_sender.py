import os, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import csv

print('Starting')
subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = input("Type your email and press enter: ")
password = input("Type your password and press enter: ")
attach = input("attach-Type your file name with Extension: ")

to_mails = input("Type csv file name: ")

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
"""
html = """\
<html>
<body>
    <p>Hi,<br>
    How are you?<br>
    <a href="https://github.com/mohamed-shaheen/automation-email-sender"><strong>my repository</strong></a> 
    help you sending many mails from csv file .
    </p>
</body>
</html>
"""
with open(attach, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part3 = MIMEBase("application", "octet-stream")
    part3.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part3)

# Add header as key/value pair to attachment part
part3.add_header(
    "Content-Disposition",
    f"attachment; filename= {attach}",
)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)
message.attach(part3)
text = message.as_string()


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    with open(to_mails+".csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        count = 0
        for name, email in reader:
            message["To"] = email
            print(f"Sending email to {name}")
            server.sendmail(sender_email, email, text)
            count+=1

print("IT'S DONE,' %s ' emails has been sent :)" %(count))