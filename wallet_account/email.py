from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

def send_confirmation_email(request, profile):
    if not profile.new_email:
        raise ValueError('profile.new_email не задан!')

    confirmation_url = request.build_absolute_uri(
        reverse('wallet_account:confirm_email', kwargs={'token': profile.confirmate_token})
    )

    send_mail(
        subject='Подтверждение изменения email',
        message=f'Перейдите по ссылке, чтобы подтвердить новы email:\n\n{confirmation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[profile.new_email],
        fail_silently=False,
    )
