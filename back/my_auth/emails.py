from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def email_reset_password_link(request, user):
    data = {
        "title": "Vérifier votre email",
        "url": (
            f"{settings.FRONT_END_URL}/nouveau-mdp?reset_key={user.reset_key.reset_key}"
        ),
    }
    send_email(
        template_directory="my_auth",
        file_name="reset_password_link",
        subject=data["title"],
        data=data,
        receiver=[user.email],
    )


def send_email(
    template_directory,
    file_name,
    subject,
    receiver,
    subject_id="",
    data=None,
    attachment=None,
):
    html = render_to_string(f"{template_directory}/emails/html/{file_name}.html", data)
    txt = render_to_string(f"{template_directory}/emails/txt/{file_name}.txt", data)
    try:
        msg = EmailMultiAlternatives(
            subject=subject_id + subject,
            body=txt,
            to=receiver,
        )

        msg.attach_alternative(html, "text/html")
        msg.extra_headers["X-Mailgun-Tag"] = [file_name]
        if attachment:
            msg.attach(attachment["name"], attachment["content"], "application/pdf")
        msg.send()
    except SMTPException as e:
        print("There was an error sending an email: ", e)
