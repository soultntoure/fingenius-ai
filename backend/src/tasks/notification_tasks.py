from celery import Celery
from ..core.config import settings
from ..services.notification_service import NotificationService
import asyncio

celery_app = Celery(
    "fingenius_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

notification_service = NotificationService()

@celery_app.task
def send_email_notification_task(user_id: int, subject: str, body: str):
    """
    Celery task to send an email notification to a user.
    """
    async def _send_email():
        # In a real implementation, you'd fetch user's email from DB using user_id
        # and then use a proper email sending library.
        print(f"Task: Sending email to user {user_id} with subject '{subject}' and body: '{body}'")
        # await notification_service.send_email(user_email, subject, body)
        await notification_service.send_notification(user_id, body, "email")
        print("Email task completed.")
    asyncio.run(_send_email())

@celery_app.task
def send_sms_notification_task(user_id: int, message: str):
    """
    Celery task to send an SMS notification to a user.
    """
    async def _send_sms():
        # In a real implementation, you'd fetch user's phone number from DB
        print(f"Task: Sending SMS to user {user_id}: '{message}'")
        # await notification_service.send_sms(user_phone, message)
        await notification_service.send_notification(user_id, message, "sms")
        print("SMS task completed.")
    asyncio.run(_send_sms())

@celery_app.task
def scheduled_daily_summary_task():
    """
    Sends a daily financial summary to users who opt-in.
    """
    # This task would query the database for users who want daily summaries
    # and then generate/send personalized summaries via send_email_notification_task
    print("Generating and sending daily financial summaries...")
    # Example: user_ids = get_users_for_daily_summary()
    # for user_id in user_ids:
    #     summary_text = generate_summary(user_id)
    #     send_email_notification_task.delay(user_id, "Your Daily FinGenius AI Summary", summary_text)
    print("Daily summary task initiated.")