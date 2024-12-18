import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, abort
import os
from jinja2 import Environment, FileSystemLoader


class Email:
    def __init__(self, sender: str, receiver: str, subject: str, message: str) -> None:
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message

    def send(self) -> None:
        if not (os.getenv("TEST_MODE", False) or os.getenv("EMAIL_TEST", False)):
            message = MIMEMultipart("alternative")
            message["Subject"] = self.subject
            message["From"] = self.sender
            message["To"] = self.receiver
            message.attach(MIMEText(self.message, "html"))
            context_ssl = ssl.create_default_context()
            try:
                with smtplib.SMTP(
                    os.getenv("SMTP_HOST", ""), int(os.getenv("SMTP_PORT", ""))
                ) as server:
                    server.ehlo()
                    if not os.getenv("DISABLE_EMAIL_TLS", False) : server.starttls(context=context_ssl)
                    server.ehlo()
                    server.login(
                        os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASSWORD", "")
                    )
                    server.sendmail(self.sender, self.receiver, message.as_string())
            except Exception as e:
                current_app.logger.critical(f"could_not_send_email [{str(e)}]")
                abort(
                    500,
                    description="We are experiencing technical difficulties. Please try again later",
                )


class Email_with_template(Email):
    def __init__(
        self, sender: str, receiver: str, subject: str, template_filename: str, **args
    ) -> None:
        # load template
        template_path = os.path.abspath(os.path.dirname(__file__)) + "/templates/email"
        if not os.path.isdir(template_path):
            raise Exception("Could not find templates directory")
        environment = Environment(loader=FileSystemLoader(template_path))
        template = environment.get_template(template_filename)
        super().__init__(sender, receiver, subject, template.render(**args))
