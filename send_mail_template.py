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
args = parser.parse_args()
print(args.filename)

def csvCheck():
    print("\n Starting CSV data check... \n")
    #variable helps print which lines the errors are located in
    i = 1
    #if even one row has an issue, allGood will be False
    allGood = True
    with open('test.csv', 'r') as file: 
        data = csv.reader(file)
        
        for line in data:
            if line[0]=="" or line[1]=="" or line[2]=="":
                #return False
                print("Issue on line " + str(i))
                allGood = False
            i+=1
        print("\n Check complete.")
        #return True
        return allGood

def send_template_email(template, to_email, subj, **kwargs):
    env = Environment(
        loader = FileSystemLoader('email_templates'),
        autoescape = select_autoescape(['html', 'xml'])
    )

    template=env.get_template(template)

    send_email(to_email, subj, template.render(**kwargs))

def send_email(to_email, subj, body):
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subj
    html_message['From'] = SENDER_EMAIL
    html_message['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, html_message.as_string())

    print("Email going to " + to_email + " has sent.")

with open(args.filename) as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        org_name=row["Organization"]
        subj=org_name + " as a SeaGL 2024 Sponsor?"

        # cascadia? returning?  result
        # no        no          regular
        # yes       no          cascadia
        # no        yes         returning
        # yes       yes         returning

        use_local_template = True if len(row["Cascadia"]) > 0 else False
        use_returning_template = True if len(row["Prev_Sponsor"]) > 0 else False

        if use_returning_template:
            template = "./SeaGL_2024_returning_sponsor_Template.html"
        elif use_local_template:
            template = "./SeaGL_2024_local_partner_Template.html"
        else:
            template = "./SeaGL_2024_Sponsor_Template.html"
            
        send_template_email(
            template=template,
            to_email=row["Contact_Email"],
            subj=subj,
            CONTACT_FIRST_NAME=row["Contact_Name"],
            SENDER_FIRST_NAME=SENDER_FIRST_NAME,
            ORG_NAME=org_name
        )
