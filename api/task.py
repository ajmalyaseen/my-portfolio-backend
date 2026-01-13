from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# Celery task to send a confirmation email to users after they submit the contact form.
@shared_task
def send_mail_users(usermail,username):
        subject = "Thank you for contacting us!"
        message = f"Hi {username}, We received your message. We will get back to you soon."
    
    
        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [usermail],
                fail_silently=False,
                )
        return "Email Sent!"
        
