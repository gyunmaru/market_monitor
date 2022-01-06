# %%
import smtplib
import json
import os
import time
# from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# %%


class Mail:

    def __init__(self, sender: str, ps: str):
        self.port = 587
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = sender
        self.password = ps

    def send(self, to_address, subject, content, attach_filename: str = ''):

        # MIME
        msg = MIMEMultipart()
        # msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self.sender_mail
        msg['To'] = to_address
        msg.attach(MIMEText(content, 'plain'))

        if attach_filename != '':
            attach_file = open(attach_filename, 'rb')
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)
            # add payload header with filename
            payload.add_header(
                'Content-Decomposition', 'attachment',
                filename=attach_filename
            )
            msg.attach(payload)

        # SMTP server
        service = smtplib.SMTP(self.smtp_server_domain_name, self.port)
        service.starttls()
        service.login(self.sender_mail, self.password)

        text = msg.as_string()
        service.sendmail(self.sender_mail, to_address, text)

        # service.send_message(msg)
        service.quit()


# %%
if __name__ == '__main__':

    with open('./info.json') as f:
        data = json.load(f)

    time_from_file_last_modified = time.time() \
        - os.path.getmtime('./monitor.pdf')

    mail = Mail(data['sender'], data['ps'])

    try:
        mail.send(
            data['to'], 'market_monitor',
            f'time from file update: {time_from_file_last_modified:.2f}',
            'monitor.pdf'
        )
        print('sent email')
    except:
        print('something went wrong')
