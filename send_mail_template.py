import smtplib

from envs import SENDER_EMAIL, SENDER_PASSWORD
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape

recipient_email = "partnerships@seagl.org"
org_name="ORG NAME"
subj=org_name + " as a SeaGL 2024 Sponsor?"
contact_first_name="CONTACT FIRST NAME"
SENDER_FIRST_NAME="SENDER FIRST NAME"

def send_template_email(template, to_email, subj, **kwargs):
    env = Environment(
        loader = FileSystemLoader('email_templates'),
        autoescape = select_autoescape(['html', 'xml'])
    )

    template=env.get_template(template)

    send_email(to_email, subj, template.render(**kwargs))

    #with open('email_template.html', 'r') as f:
    #    template = Template(f.read())

def send_email(to_email, subj, body):
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subj
    html_message['From'] = SENDER_EMAIL
    html_message['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, html_message.as_string())

    print("Email going to " + to_email + " has sent.")

send_template_email(
    template='SeaGL_2024_Sponsor_Template.html',
    to_email=recipient_email,
    subj=subj,
    CONTACT_FIRST_NAME=contact_first_name,
    SENDER_FIRST_NAME=SENDER_FIRST_NAME,
    ORG_NAME=org_name
)