import resend
from core.utils.config import settings

resend.api_key = settings.RESEND_API_KEY
def send_email(to_email: str, subject: str, content: str):
    resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": to_email,
        "subject": subject,
        "html": f"<p>{content}</p>"
    })

