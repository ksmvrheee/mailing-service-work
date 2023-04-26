from django.urls import path

from .views import *


urlpatterns = [
    path('api/v1/customer/', CustomerAPICreator.as_view()),
    path('api/v1/customer/<int:pk>/', CustomerAPIManager.as_view()),
    path('api/v1/mailing/', MailingAPICreator.as_view()),
    path('api/v1/mailing/<int:pk>/', MailingAPIManager.as_view()),
    path('api/v1/mailing_statistic/', MailingStatistic.as_view()),
    path('api/v1/mailing_statistic/<int:pk>/', MailingStatistic.as_view()),
    path('api/v1/mailing_start/<int:pk>/', MailingStarterView.as_view()),
    path('api/v1/mailing_delete/<int:pk>/', MailingDeleterView.as_view()),
]
