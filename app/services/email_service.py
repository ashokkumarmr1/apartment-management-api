from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings


class EmailService:

    @staticmethod
    def send_otp(
        recipient: str,
        otp: str,
    ):

        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=recipient,
            subject="Apartment Management - Password Reset OTP",
            plain_text_content=(
                f"Your password reset OTP is: {otp}\n\n"
                "This OTP is valid for 5 minutes."
            ),
        )

        try:
            sg = SendGridAPIClient(
                settings.SENDGRID_API_KEY
            )

            response = sg.send(message)

            print(
                f"OTP email sent to {recipient}. "
                f"Status: {response.status_code}"
            )

        except Exception as e:
            print(f"Email sending failed: {e}")
            raise