from datetime import datetime
from email.mime.text import MIMEText
import smtplib, ssl

from .scheduling import scheduler
from .models import Message, Customer, Mailing
from .secret import SERVER, PORT, EMAIL, PASSWORD


def start_mailing(mailing):
    print(f'Started mailing #{mailing.pk}!')

    customers_list = list(Customer.objects.filter(tag=mailing.customer_tag))

    k = len(customers_list)

    mailing_text = mailing.text
    mailing_subject = mailing.subject

    while datetime.now().timestamp() < mailing.finish_datetime.timestamp() and k:
        i = k - 1

        current_msg = Message.objects.create(
            creating_datetime=datetime.now(),
            status=False,
            corresponding_mailing=mailing,
            corresponding_customer=customers_list[i]
        )
        current_msg.save()

        try:
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
                server.login(EMAIL, PASSWORD)

                message = MIMEText(mailing_text.format(name=customers_list[i].name))

                message['Subject'] = mailing_subject.format(name=customers_list[i].name)
                message['From'] = EMAIL
                message['To'] = recipient =customers_list[i].personal_email

                server.sendmail(EMAIL, [recipient,], message.as_string())
                server.quit()

        except (smtplib.SMTPHeloError, smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused, smtplib.SMTPDataError,
                smtplib.SMTPNotSupportedError) as e:
            print(e)

        else:
            current_msg.status = True
            current_msg.save()

        k -= 1

    print(f'Finished mailing #{mailing.pk}!')


def delete_mailing(pk):
    m = Mailing.objects.filter(pk=pk)

    if not m:
        return {'error': 'Can\'t find Mailing with such id!'}

    elif m[0].launch_datetime.timestamp() < datetime.now().timestamp() < m[0].finish_datetime.timestamp():
        try:
            scheduler.remove_job(f'mailing_{pk}')
        except:
            m[0].delete()

    m[0].delete()

    return {'message': 'Mailing was successfully deleted.'}
