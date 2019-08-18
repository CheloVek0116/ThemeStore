from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def OrderCreated(order_id):
    """
    Отправка Email сообщения о создании покупке
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ c номером %s' % order.id
    message = 'Дорогой, %s, вы успешно сделали заказ.\
               Номер вашего заказа %s' % (order.user.first_name, order.id)
    mail_send = send_mail(subject, message, 'admin@myshop.ru', ['admin@myshop.ru'])
    return mail_send