class NotificationService:
    def __init__(self):
        # Initialize email/SMS client here (e.g., SendGrid, Twilio)
        pass

    async def send_notification(self, user_id: int, message: str, notification_type: str = "email"):
        """
        Sends a notification to the user via specified channel.
        """
        # Placeholder: Fetch user contact info from DB
        # user_email = ...
        # user_phone = ...

        print(f"Sending {notification_type} notification to user {user_id}: {message}")
        if notification_type == "email":
            # Logic to send email
            pass
        elif notification_type == "sms":
            # Logic to send SMS
            pass
        # Future: in-app notifications, push notifications
        print("Notification sent.")

    async def notify_automation_pending_approval(self, user_id: int, suggestion_details: dict):
        """
        Notifies user that an automated action requires their approval.
        """
        message = f"FinGenius AI has a new financial suggestion for you: {suggestion_details.get('description')}. Please review and approve in the app."
        await self.send_notification(user_id, message, "email")
