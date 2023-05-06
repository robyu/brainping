# BRAINPING

A Descriptive Experience Sampling Method

## ## Intro

After reading [Temple Grandin's book on Visual Thinking](https://www.templegrandin.com/templegrandinbooks.html), I was inspired to try Russell Hurlbert's Descriptive Experience Sampling (DES) -- [wikipedia entry](https://en.wikipedia.org/wiki/Descriptive_Experience_Sampling)-- on myself to determine my cognitive style.  The intent of DES is to capture a person's inner experience--thoughts, perceptions--at random times throughout the day; this method avoids the mental editing associated with retrospection. 

Grandin asserts that people can be sorted into roughly three bins according to their dominant "cognitive style":

* "object visualizers" are a subset of "visual thinkers." Object visualizers, of which Grandin is an example, think in terms of concrete, detailed images and tend toward spatial reasoning.  Visual thinkers tend to be mechanically inclined. Grandin lists graphics designers, artists, tradespeople, architects, inventors, and mechanical engineers as typical object visualizers.

* "verbal thinkers" rely on language: sequential, linear, word-based thinking.  Supposedly, they are good at general organization and "talk" to themselves. Grandin lists teachers, lawyers, writers, policitians, and administrators as typical verbal thinkers.

* "spatial visualizers" are mathematically inclined visual thinkers who process in terms of patterns and relationships. According to Grandin, scientists, statisticians, electrical engineers, and physicists are typical spatial visualizers.

Grandin says that these cognitive styles have some interesting, perhaps severe, societal ramifications. For example, Grandin asserts that it's a verbal thinkers's world because of their superior social communication skills, as well as their tendency to do well on standardized tests. In addition, she says that object visualizers have trouble with algebra in school, because it's too abstract. 

## Method

In Hurlburt's original method, participants carried devices which beeped at random times throughout the day. Upon hearing the beep, the participant note their inner experience directly before the beep. At the end of the day, a researcher collects the notes and does a follow-up interview to expand or clarify the notes--this must be done with 24 hours to avoid the editing and loss associated with mental recall.

With smartphones, everybody is essentially carrying a beeper at all times, as well as the means to take notes.  My software, Brainping, merely schedules and sends the "beep" to your phone.

## Results

What cognitive style am I? I'm an electrical engineer; I'm not great at math, but maybe I'm better than the average bear. When I'm doing technical work, I definitely manipulate pictures on my head (or on paper, really). Finally, I've long noticed that after any extended period of technical work, say after an intense day in the office, I had short-term aphasia. Sitting at the dinner table, words simply would not come to mind.

I ran brainping for 8 days, with 6 beeps per day. Here's a typical note:

```
ping (1 / 6) @ 2023-02-09 10:23:00
I had just completed a turn through an intersection  while listening 
to Tom Pettys won’t back down. I pictured him performing in a dark stage
 in Los Angeles. I was smugly musing that Tom escaped  Gainesville,
 like I did. This was a feeling, an emotion--no words.  I was conscious of the steering 
wheel in my left hand. I wasn’t really paying attention to the street. 
```

In a nutshell, there aren't many words going through my head. There's very little internal dialogue, i.e. "self-talk." Instead, I see or feel images, sometimes short videos. My brain works like TikTok. :-(

## Setup

First you'll need a SMTP server to send email from your computer with SSL and TSL. If you have a gmail account, you can use Google's SMTP server. See https://support.google.com/a/answer/176600?hl=en for instructions on configuring your gmail account.

Second, you need to be able to receive email messages as text messages on your phone. Most major wireless carriers have a "SMS Gateway": by sending an email to a specific email address, it will arrive at your phone as a SMS message; for example, Verizon uses <phonenumber>@vtext.com. This article lists gateways for common carriers: [SMS Gateway: From Email to SMS Text Message](https://www.lifewire.com/sms-gateway-from-email-to-sms-text-message-2495456)

Copy config-template.json to config.json and edit config.json to specify your emailer parameters:

- smtp_server: the SMTP server address
- smtp_port: the SMTP server port, typically 465
- email_user: the "from" email address; equivalent to your SMTP server login
- email_dest: the destination email address, i.e. the email-to-SMS gateway

Create a text file, e.g. "email-passwd.txt", which contains the SMTP server's login password.

You must also edit config.json to specify:

- start_time: the start time to start sending brainpings in HH:MM:SS format, e.g. "09:00:00" for 9:00:00 am
- stop_time: the stop time for sending brainpings, again in HH:MM:SS format
- num_pings: the number of brainpings to within the start-stop interval

Based on Hurlburt's recommendations, on your phone you should assign a unique alert sound to messages which arrive from email_user; this drives a different behavior than "answer that text message." Search the web for "assign unique tone to text message."

## Usage

Assuming that you've created ```config/config.json``` and ```config/email-pwd.txt``` and you are in the top-level ```./brainping``` directory:

**Test the SMTP -SMS Gateway connection**: send a test message, then quit

```
python src/brainping.py config/config.json config/email-pwd.txt --debug-send
```

You should see SMTP connection stuff:

```
10:03:25.027805 send: 'ehlo 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa\r\n'
10:03:25.054916 reply: b'250-smtp.gmail.com at your service, [73.231.4.177]\r\n'
...
10:03:25.511030 send: b"\r\nSubject: brainping send test\r\n\r\..."
...
10:03:26.189139 reply: retcode (221); Msg: b'2.0.0 closing connection v13-20020a170903238d00b001aafdf8063dsm3881673plh.157 - gsmtp'
```

**Run brainping**:

```
python src/brainping.py config/config.json config/email-pwd.txt
```

Upon executing, brainping will print the randomly selected ping schedule for that day, send the beeps, then stop at the configured time. Note that brainping.py only runs for one day.

```
ping schedule:
 0 2023-05-06 11:05:00
 1 2023-05-06 11:15:00
 2 2023-05-06 13:31:00
 3 2023-05-06 15:31:00
 4 2023-05-06 16:55:00
 5 2023-05-06 17:27:00

starting time 2023-05-06 10:06:46.696220
```

**Print help**

```
python brainping.py --help
```

## Unit Tests

```
python -m unittest
```

```
python -m unittest tests/test_mqttif.py  # by file
```

for the following, you must first cd into ./tests

```
python -m unittest test_mqttif # by module

python -m unittest test_mqttif.TestMqttIf # by class

python -m unittest test_mqttif.TestMqttIf.test_pub_rcv  # by method
```
