import smtplib
import csv
import argparse

from envs import SENDER_EMAIL, SENDER_PASSWORD, SENDER_FIRST_NAME
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser(prog="send_mail_template.py",
    description="Sends an email based on template.")
parser.add_argument('filename')
parser.add_argument('partner_type')
args = parser.parse_args()
print(args.filename)
print(args.partner_type)

def send_template_email(template, signature, to_email, subj, cc, **kwargs):
    env = Environment(
        loader = FileSystemLoader('email_templates'),
        autoescape = select_autoescape(['html', 'xml'])
    )

    template=env.get_template(template)
    signature = env.get_template(signature)

    send_email(to_email, subj, cc, template.render(**kwargs),signature.render(**kwargs))

def send_email(to_email, subj, cc, body, signature):
    
    html_message = MIMEMultipart()
    html_message.attach(MIMEText(body, 'html'))
    html_message.attach(MIMEText(signature, 'html'))
    html_message['Subject'] = subj
    html_message['From'] = SENDER_EMAIL
    html_message['To'] = to_email
    html_message['Cc'] = cc

    with smtplib.SMTP_SSL('mail.seagl.org', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, html_message.as_string())

    print("Email going to " + to_email + " has sent.")

with open(args.filename) as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        org_name=row["Organization"]
        if (args.partner_type == "sponsor"):
            subj=org_name + " as a SeaGL 2025 Sponsor?"
        elif (args.partner_type == "partner"):
            subj=org_name + " as a SeaGL 2025 Partner?"
        elif (args.partner_type == "reminder"):
            subj="Checking in about " + org_name + " as a SeaGL 2025 Partner?"
        else:
            print ("Warning: partner type incorrectly input or inexistent.")
            print ("Current checks are for..")
            print (" - sponsor")
            print (" - partner")


        # cascadia? returning?  result
        # no        no          regular
        # yes       no          cascadia
        # no        yes         returning
        # yes       yes         returning

        use_local_template = True if len(row["Cascadia"]) > 0 else False
        use_returning_template = True if len(row["Prev_Sponsor"]) > 0 else False
        use_reminder_template = True if args.partner_type == "reminder" else False

        if use_reminder_template:
            template = "./reminder_Template.html"
        elif use_returning_template:
            template = "./returning_sponsor_Template.html"
        elif use_local_template:
            template = "./local_partner_Template.html"
        elif use_local_template:
            template = "./local_partner_Template.html"
        else:
            template = "./sponsor_Template.html"

        signature = "./signature_Template.html"

        cc_email="partnerships@seagl.org"

        send_template_email(
            template=template,
            signature=signature,
            to_email=row["Contact_Email"],
            subj=subj,
            cc=cc_email,
            CONTACT_FIRST_NAME=row["Contact_Name"],
            SENDER_FIRST_NAME=SENDER_FIRST_NAME,
            ORG_NAME=org_name
        )
