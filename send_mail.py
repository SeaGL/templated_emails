import smtplib

from envs import SENDER_EMAIL, SENDER_PASSWORD
from email.mime.text import MIMEText
from jinja2 import Template

recipient_email = "partnerships@seagl.org"

with open('email_template.html', 'r') as f:
    template = Template(f.read())

context = {
    'CONTACT_FIRST_NAME': 'FIRST NAME',
    'ORG_NAME': 'ORG NAME',
    'SENDER_FIRST_NAME': 'SENDER NAME'
}

html = template.render(context)

# TODO: Below needs fixing for better templating
html_message = MIMEText(context['body'], 'html')
html_message['Subject'] = context['subject']
html_message['From'] = SENDER_EMAIL
html_message['To'] = recipient_email

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, recipient_email, html_message.as_string())

print("Email going to " + recipient_email + " has sent.")
