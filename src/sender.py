import smtplib
import ssl
from pathlib import Path

class Sender():
    def __init__(self,
                 email_user = '',
                 email_pwd_fname = None,
                 smtp_server = "smtp.gmail.com",
                 smtp_port = 465):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.debuglevel=0

        assert Path(email_pwd_fname).exists()
        with open(email_pwd_fname, "r") as f:
            self.email_pwd = f.read()
        #

    def send(self, dest_addr, subject, body):
        ssl_context = ssl.create_default_context()

        assert len(subject) > 0
        assert len(body) > 0
        msg = f"""
Subject: {subject}

{body}"""
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=ssl_context) as server:
            server.set_debuglevel(self.debuglevel)
            server.login(self.email_user, self.email_pwd)
            server.sendmail(self.email_user,
                            dest_addr,
                            msg)
        #


        
    
                 
