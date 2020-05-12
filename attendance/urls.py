from django.conf.urls import url
from attendance import views

urlpatterns = [
    url('^detect/$', views.detect),
]