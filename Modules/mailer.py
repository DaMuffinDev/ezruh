from Resources.required_modules import pymodules
pymodules.install(pymodules.presets.modules("mailer"))

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

class Mailman:
    plain = "plain"
    html = "html"
    def __init__(self, sender_address, sender_password, port):
        self.sender_address = sender_address
        self.sender_password = sender_password
        self.port = port
        self.context = ssl.create_default_context()
    
    def send(self, reciever_address, data):
        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=self.context) as server:
            server.login(self.sender_address, self.sender_password)
            server.sendmail(self.sender_address, reciever_address, data)
    
    def format_mail(self, subject, content, reciever_address, content_type=plain):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_address
        message["To"] = reciever_address
        message.attach(MIMEText(content, content_type))
        return message.as_string()

def mailman_data(sender, password, port):
    class MailmanDataObject:
        def __init__(self, sender, password, port):
            self.sender = sender
            self.password = password
            self.port = port
    return MailmanDataObject(sender, password, port)

def mailman_message(subject, message, content_type=Mailman.plain):
    class MailmanMessageObject:
        def __init__(self, subject, message, content_type):
            self.subject = subject
            self.message = message
            self.content_type = content_type
    return MailmanMessageObject(subject, message, content_type)

# Repeated mailing to a single address
def mail_repeated_address(message_object, data_object, reciever_address, repeat_amount=1):
    """
    :param message_object - mailman_message("test subject", "test body", Mailman.plain)
    :param data_object - mailman_data("test@gmail.com", "password", repeated_amount=5)
    :param reciever_address - The address to send the mail to
    :param repeat_amount - The amount of times the email will be sent
    """

    mailer = Mailman(data_object.sender, data_object.password, data_object.content_type)
    for index in range(0, repeat_amount, 1):
        mailer.send(reciever_address, \
            mailer.format_mail(message_object.subject, message_object.message, reciever_address, message_object.content_type))