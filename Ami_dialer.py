#!/usr/bin/env python

import socket
import smtplib
from email.MIMEText import MIMEText
import os
import sys

no_need_send = "/home/emilius/pyprojects/no_need_send"

def send_mail(subject, text):
    import smtplib
    from email.MIMEText import MIMEText
    msg = MIMEText(text, "", "utf-8")
    #msg['Subject']='Call failed'
    msg['Subject'] = subject
    #msg['Subject'] = h_cause
    msg['From']='Auto Dialer'
    sender = 'e.omin@corp.mastertel.ru'
   #recipients = ['voice@tel.ru', 'help@tel.ru']
    recipients = ['voice@rtel.ru']
    msg['To']=", ".join(recipients)
    mailSrv=smtplib.SMTP("mail.tel.ru",25)
    mailSrv.ehlo()
    mailSrv.sendmail(sender, recipients, msg.as_string())
    mailSrv.close()


s = socket.socket()
s.connect(("10.100.100.104", 5038))
s.send("Action: login\r\nUsername: pbx\r\nSecret: testpbx123\r\n\r\n")

sip_show_reg = "Action: SIPshowregistry\r\nActionId: 0000999\r\n\r\n"

s.send(sip_show_reg)
ans = ''
while 1:
    ans += s.recv(1)
    h = ans.find('Event: RegistrationsComplete\r\n')
    if h > -1:
        if ans.find('\r\n\r\n', h + 1) > -1:
            break

l = ans.split("/r/n/r/n")
for i in range(len(l)):
    if l[i].find("RegistryEntry") > -1:
        if l[i].find("253-mastertel") > -1:
            if l[i].find("State: Registered") > -1:
                print "registered"
            else:
                print "not registered"
                text = "253-mastertel not registered"
                #os.system('asterisk -x "sip reload"')
                if os.path.exists(no_need_send) == False:
                    print send_mail("Not registered", text)    
                    print "mail sended"
                    f = open(no_need_send, 'w')
                    f.write('0')
                    f.close()
                print os.system('asterisk -x "sip reload"')
                
                sys.exit()



call = """Action: Originate\r
ActionId: 00001\r
Channel: SIP/master-o/85020000000\r
Exten: 777\r
Context: office\r
Priority: 1\r
Callerid: 3331111111\r
Timeout: 30000\r
\r

"""

s.send(call)
ans = ''
while 1:
    ans += s.recv(1)
    h = ans.find('Event: Hangup\r\n')
    if h > -1:
        if ans.find('\r\n\r\n', h + 1) > -1:
            break

h1 = ans.find("Cause", h)
h2 = ans.find("/r/n/r/n", h+1)
h_cause = ans[h1:h2]
print h_cause



if (os.path.exists(no_need_send) == False) and (ans.find("Normal Clearing", h) == -1):
    text = "Atencion\r\n\r\n"
    text += "call from 253-mastertel to 85020000000 Failed \r\n\r\n"
    text += h_cause + "\r\n"
    subject = 'Call Failed'
    send_mail(subject, text)
    f = open(no_need_send, 'w')
    f.write('0')
    f.close()
if os.path.exists(no_need_send) and (ans.find("Normal Clearing", h) > -1):
    os.remove(no_need_send)
    text = ""
    text += "call from 253-mastertel to 85020000000 successful \r\n\r\n"
    text += h_cause + "\r\n"
    subject = "Recovered"
    send_mail(subject, text)
# logof from AMI
logof = "Action: Logoff\r\n\r\n"
s.send(logof)
s.close()


