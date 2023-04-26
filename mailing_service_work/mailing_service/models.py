from django.core.validators import EmailValidator
from django.db import models


class Mailing(models.Model):
    launch_datetime = models.DateTimeField()
    finish_datetime = models.DateTimeField()
    text = models.TextField()
    subject = models.CharField(max_length=255)
    customer_tag = models.CharField(max_length=255)

    def __str__(self):
        return f'Mailing due to {self.launch_datetime}.'


class Customer(models.Model):
    name = models.CharField(max_length=255)
    personal_email = models.EmailField(unique=True, validators=[EmailValidator()])
    tag = models.CharField(max_length=255)

    def __str__(self):
        return f'Customer {self.name} ({self.tag}) with an email: {self.personal_email}.'


class Message(models.Model):
    creating_datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    corresponding_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    corresponding_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
