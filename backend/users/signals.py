import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from .models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_email_verification(sender, instance: User, created, **kwargs):
    if created and not instance.email_verified:
        subject = "[aviCable] " + _("confirm_email.mail.subject")
        message = _("confirm_email.mail.message").format(
            name=instance.full_name,
            url=settings.SITE_URL,
            token=instance.registration_token,
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created and instance.email_verified and instance.is_active:
        subject = "[aviCable] " + _("welcome.mail.subject")
        message = _("welcome.mail.message").format(
            name=instance.full_name, url=settings.SITE_URL
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def send_activation_email_to_admin(sender, instance, created, **kwargs):
    if not created and instance.email_verified and not instance.is_active:
        recipients = [
            user
            for user in User.objects.filter(is_staff=True)
            .filter(is_active=True)
            .filter(areas__in=instance.areas.all())
        ]
        if not recipients:
            recipients = [
                user for user in User.objects.filter(is_superuser=True)
            ]

        subject = "[aviCable] " + _("subscription.mail.subject")
        message = _("subscription.mail.message").format(
            name=instance.full_name,
            url=settings.SITE_URL,
            token=instance.registration_token,
        )

        from_email = settings.EMAIL_HOST_USER

        recipient_list = [user.email for user in recipients]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            instance.groups.add(Group.objects.get(name="data-read-only"))
        except Group.DoesNotExist as _e:
            logger.error(_e)
