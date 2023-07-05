
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime, timedelta
from config import settings







def send_email(email, message, phone):
    
    
    

    # me == my email address
    # you == recipient's email address
    me = settings.sender
    you = settings.receiver
    password = settings.password
   
    



    html = f"""\
        <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            
            <div>
            <p> Email: {email} </p>
            <p> Phone Number: {phone} </p>
            <p> Message: {message} </p>
        </div>
            </body>
            </html>
        """
    msg = MIMEMultipart()

    msg['Subject'] = "Notification mail"
    msg['From'] = me
    msg['To'] = you

    msg.attach(MIMEText(html,"html"))
    msg_string = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as server:
        server.login(me, password)
        server.sendmail(me, you, msg_string)




