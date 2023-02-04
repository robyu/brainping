# BRAINPING

## Setup 
First you'll need a SMTP server to send email from your computer with SSL and TSL. If you have a gmail account, you can use Google's SMTP server. See https://support.google.com/a/answer/176600?hl=en for instructions on configuring your gmail account.

Second, you need to be able to receive email messages as text messages on your phone. Most major wireless carriers have a "SMS Gateway": by sending an email to a specific email address, it will arrive at your phone as a SMS message; for example, Verizon uses <phonenumber>@vtext.com.

Copy config-template.json to config.json and edit config.json to specify your emailer parameters:
- smtp_server: the SMTP server address
- smtp_port: the SMTP server port, typically 465
- email_user: the "from" email address
- email_dest: the destination email address, i.e. the email-to-SMS gateway

Create a text file, e.g. "email-passwd.txt", which contains the SMTP server's login password.

You must also edit config.json to specify:
- start_time: the start time to start sending brainpings in HH:MM:SS format, e.g. "09:00:00" for 9:00:00 am
- stop_time: the stop time for sending brainpings, again in HH:MM:SS format
- num_pings: the number of brainpings to within the start-stop interval

## Usage
Assuming that you've created config/config.json and config/email-pwd.txt:

Run brainping: the script will execute and send brainpings until stop_time, then quit.
```
python brainping.py config/config.json config/email-pwd.txt
```

Test the SMTP server: send a test message, then quit
```
python brainping.py config/config.json config/email-pwd.txt --debug-send-msg
```

Print help
```
python brainping.py --help
```

## Unit Tests
python -m unittest

python -m unittest tests/test_mqttif.py  # by file

#
# for the following, you must first cd into ./tests
python -m unittest test_mqttif # by module

python -m unittest test_mqttif.TestMqttIf # by class

python -m unittest test_mqttif.TestMqttIf.test_pub_rcv  # by method




