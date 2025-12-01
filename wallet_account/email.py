from django.core.mail import send_mail, get_connection
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

def update_confirmation_email(request, profile):
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

def create_confirmation_email(user, token):
    try:
        link = settings.BASE_URL + reverse('wallet_account:confirm_email', kwargs={'token': token})
    
        conection = get_connection(timeout=30)
        send_mail(
            subject='Подтвердите email',
            message=(
                f'Здравствуйте!\n\n'
                f'Для активации аккаунта перейдите по ссылке:\n'
                f'{link}\n\n'
                'Ссылка действительна 24 часа.\n\n'
                'Еслиы вы не регистрировались на нашем сайте - проигнорируйте это письмо.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            connection=conection,
            fail_silently=False,
        )
    except Exception as e:
        messages.error(f'Ошибка отправки письма пользователю {user.email}: {e}')
        raise