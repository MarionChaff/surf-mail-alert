import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailNotifier:

    """
    A class to send email notifications using a SMTP server.

    Attributes
    ----------
    smtp_server : str; the address of the SMTP server.
    smtp_port : int; the port number to use for the SMTP server (standard in SMTP protocol: 587).
    email_user : str; the email address used to send emails.
    email_password : str, the password for the email account.

    Methods
    -------
    send_email(recipient, subject, body) : sends an email to the specified recipient with the given subject and body.

    """

    def __init__ (self, smtp_server, smtp_port, email_user, app_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.app_password = app_password

    def send_email(self, recipient, subject, html_body, image_path=None):

        alert = MIMEMultipart('alternative')
        recipient = recipient
        alert['From'] = self.email_user
        alert['To'] = recipient
        alert['Subject'] = subject

        alert.attach(MIMEText(html_body, 'html'))

        # Attach image if provided
        if image_path:
            try:
                with open(image_path, 'rb') as img:
                    image = MIMEImage(img.read())
                    image.add_header('Content-ID', '<image1>', filename="tides.jpg")
                    alert.attach(image)
            except Exception as e:
                print(f"🚨 Error attaching image: {e}")

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.app_password)
            text = alert.as_string()
            server.sendmail(self.email_user, recipient, text)
            server.quit()
        except Exception as e:
            print(f"🚨 Error: {e}")

        return None
