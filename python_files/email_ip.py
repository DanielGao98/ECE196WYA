import smtplib
import os

reciever = input()

def get_ip():
    return os.popen('hostname -I').read().split[0]

def send(reciever = reciever):
    sender = 'wya196wya@gmail.com'
    password = 'wya196wya'

    #Send the mail
    msg = "\n"+get_ip()  # The /n separates the message from the headers


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, reciever, msg)

send()
