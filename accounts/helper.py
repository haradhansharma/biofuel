from django.core.exceptions import PermissionDenied
from evaluation.models import *
from accounts.models import *
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.core.mail import mail_admins, send_mail, send_mass_mail


class CustomsernameValidator(UnicodeUsernameValidator, ASCIIUsernameValidator):
    """
    Custom username validator that allows only letters, numbers, and periods.
    """

    regex = r'^[\w.]+\Z'

    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and periods.'
    )


# The function is abandoned and no where using currently.
def check_type(request, slug):
    """
    Checks if the current user has the permission to access the requested resource.

    Args:
        request (django.http.HttpRequest): The HTTP request object.
        slug (str): The slug of the user type.

    Raises:
        PermissionDenied: If the current user does not have the permission to access the requested resource.
    """

    try:
        curnt_user_type_slug = request.user.usertype.slug
    except Exception as e:  # pylint: disable=broad-except
        curnt_user_type_slug = None

    if curnt_user_type_slug == slug or request.user.is_staff or request.user.is_superuser:
        pass
    else:
        raise PermissionDenied


def send_admin_mail(subject, message):
    """
    Sends an email to all admins.

    Args:
        subject (str): The email subject.
        message (str): The email message.
    """

    from .models import User

    admins = User.objects.filter(is_staff=True, is_active=True)
    email_recipent = []
    for admin in admins:
        email_recipent.append(admin.email)

    send_all_email = [(subject, message, settings.DEFAULT_FROM_EMAIL, [e]) for e in email_recipent]
    send_mass_mail((send_all_email), fail_silently=False)
    

    