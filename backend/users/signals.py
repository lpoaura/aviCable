import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_email_verification(sender, instance, created, **kwargs):
    if created and not instance.email_verified:
        subject = _("Email Verification for Your Account")
        message = _(
            f"""Hello,\n\nYou asked for a registration on {settings.SITE_URL}.\n
Please click the link below to verify your email address :\n\n
{settings.SITE_URL}/account/check_email?token={instance.registration_token}
            """
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email_verified and instance.is_active:
        print()
        subject = "Welcome to Our Website"
        message = f"Hello {instance.email},\n\nWelcome to our website! Thank you for joining us."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def send_activation_email_to_admin(sender, instance, created, **kwargs):
    logger.debug(f"<send_activation_email_to_admin> sender {sender}")
    logger.debug(f"<send_activation_email_to_admin> instance {instance}")
    logger.debug(f"<send_activation_email_to_admin> created {created}")
    logger.debug(f"<send_activation_email_to_admin> kwargs {kwargs}")
    if created and instance.email_verified and not instance.is_active:
        recipients = [
            user.email
            for user in User.objects.filter(is_staff=True)
            .filter(is_active=True)
            .filter(areas__in=instance.areas)
        ]
        if not recipients:
            recipients = [
                user.email for user in User.objects.filter(is_superuser=True)
            ]

        print(recipients)
        subject = _("A new user to active have been registered")
        message = _(
            f"""Hello,\n\n
A new user have been registered on {settings.SITE_URL} and require an activation.\n\n
Please go to to process activation :\n\n
{settings.SITE_URL}/account/activate?token={instance.registration_token}
"""
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in recipients]
        send_mail(subject, message, from_email, recipient_list)
