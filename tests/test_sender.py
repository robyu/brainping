import sys
sys.path.insert(0, './tests')
sys.path.insert(0, './src')

import unittest
import json
import sender

class TestSender(unittest.TestCase):
    def load_config_dict(self):
        with open("tests/config.json", "r") as f:
            config_d = json.load(f)

        return config_d['sendertest']
        
    def test_smoke(self):
        config_d = self.load_config_dict()
        #
        #
        s = sender.Sender(email_user = config_d['email_user'],
                          email_pwd_fname = 'tests/email-pwd.txt')
        self.assertTrue(True)

    def test_send_message(self):
        config_d = self.load_config_dict()

        s = sender.Sender(email_user = config_d['email_user'],
                          email_pwd_fname = 'tests/email-pwd.txt')

        subject = "test message"
        body = "doctor's orders!"
        
        s.send(config_d['dest_addr'],
               subject,
               body)

        self.assertTrue(True)
        

