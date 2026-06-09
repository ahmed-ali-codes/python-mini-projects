"""
email_notifier.py — Send email notifications via smtplib (SMTP/TLS).

Supports:
  - Plain text and HTML emails
  - File attachments
  - Gmail and custom SMTP servers
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def send_email(
    smtp_host: str,
    smtp_port: int,
    sender_email: str,
    sender_password: str,
    recipient: str,
    subject: str,
    body: str,
    html: bool = False,
    attachments: list[str] | None = None,
) -> bool:
    """
    Send an email via SMTP with STARTTLS.

    Args:
        smtp_host:        SMTP server hostname (e.g. 'smtp.gmail.com')
        smtp_port:        SMTP port (587 for STARTTLS)
        sender_email:     Sender's email address
        sender_password:  Sender's password or app password
        recipient:        Recipient email address
        subject:          Email subject line
        body:             Email body (plain text or HTML)
        html:             If True, send body as HTML
        attachments:      Optional list of file paths to attach

    Returns:
        True on success, raises exception on failure.
    """
    msg = MIMEMultipart("alternative" if html else "mixed")
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject

    content_type = "html" if html else "plain"
    msg.attach(MIMEText(body, content_type, "utf-8"))

    # Attach files
    for filepath in (attachments or []):
        path = Path(filepath)
        if not path.is_file():
            print(f"  ⚠️  Attachment not found: {filepath}")
            continue
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')
        msg.attach(part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())

    return True


def build_html_body(title: str, lines: list[str]) -> str:
    """Build a simple styled HTML email body."""
    items = "".join(f"<li style='margin:4px 0'>{line}</li>" for line in lines)
    return f"""
    <html><body style="font-family:Arial,sans-serif;color:#1e293b;padding:20px">
      <div style="background:#1d4ed8;color:white;padding:14px 20px;border-radius:6px 6px 0 0">
        <h2 style="margin:0">{title}</h2>
      </div>
      <div style="background:#f8fafc;padding:20px;border:1px solid #e2e8f0;border-radius:0 0 6px 6px">
        <ul style="padding-left:18px">{items}</ul>
      </div>
      <p style="color:#94a3b8;font-size:11px;margin-top:12px">
        Sent by Task Automation Suite
      </p>
    </body></html>
    """
