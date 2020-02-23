import smtplib
import os

def get_ip():
    return os.popen('hostname -I').read().split()[0]

def send():
    sender = 'wya196wya@gmail.com'
    password = 'wya196wya'
    reciever = 'wya196wya@gmail.com'
    #Send the mail
    msg = "\n"+get_ip()  # The /n separates the message from the headers


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, reciever, msg)

send()
