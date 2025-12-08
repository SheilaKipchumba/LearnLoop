from django.urls import path, include
from . import views

app_name = "payments"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("initiate/<int:loop_id>/", views.initiate_payment, name="initiate"),
    path("buy/<int:loop_id>/", views.initiate_payment, name="buy_loop"),  
    path("success/", views.payment_success, name="success"),
    path("mpesa-callback/", views.mpesa_callback, name="mpesa_callback"),
]
