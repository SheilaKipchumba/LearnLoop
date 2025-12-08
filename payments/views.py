import json
import requests
import base64
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Payment
from loops.models import Loop
from django_daraja.mpesa.core import MpesaClient




"""
============================
 M-PESA CONFIG (MOVE TO .env)
============================
"""
MPESA_CONSUMER_KEY = "QIIabyOC4ZKYOKMHLfgZwGlHt7dzGJOBQbscF9hFMhPFvNKi"
MPESA_CONSUMER_SECRET = "GilorS2HyArZGzfYGBS8rKDhi4yYHX5OswqdJl1fIvA6z1nGEDgw218GYrftpFbf"
MPESA_SHORTCODE = "174379"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CALLBACK_URL = 'https://api.darajambili.com/express-payment'


def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '07xxxxxxxx'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)



def get_mpesa_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    return response.json().get("access_token")


"""
============================
 STEP 1: User clicks BUY
============================
"""
@login_required
def buy_loop(request, loop_id):
    loop = get_object_or_404(Loop, pk=loop_id)

    # If already purchased → redirect
    if request.user in loop.is_purchased_by.all():
        return redirect("loop_detail", pk=loop.pk)

    return redirect("initiate_payment", loop_id=loop.id)



"""
============================
 STEP 2: Enter phone & send STK Push
============================
"""
@login_required
def initiate_payment(request, loop_id):
    loop = get_object_or_404(Loop, pk=loop_id)

    if request.method == "POST":
        cl = MpesaClient
        phone = request.POST.get("phone")

        # CREATE PAYMENT RECORD
        payment = Payment.objects.create(
            user=request.user,
            loop=loop,
            phone_number=phone,
            amount=loop.price,
            status="Pending"
        )

        # Generate access token
        access_token = get_mpesa_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create password for M-Pesa
        password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        # STK PUSH URL
        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(loop.price),
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "phone_number": phone,
            "callback_url": "https://api.darajambili.com/express-payment",
        
            "account_reference": f"Loop-{loop.id}",
            "transaction_desc": "Payment for Premium Loop Access"
        }

        # Send request
        mpesa_response = requests.post(stk_url, json=payload, headers=headers).json()

        payment.checkout_request_id = mpesa_response.get("CheckoutRequestID")
        payment.merchant_request_id = mpesa_response.get("MerchantRequestID")
        payment.save()
        mpesa_client = MpesaClient()  
        response = mpesa_client.stk_push(phone_number= phone,
            callback_url='https://api.darajambili.com/express-payment',
        
            account_reference= f"Loop-{loop.id}",
            transaction_desc= "Payment for Premium Loop Access",  
            amount=loop.price)
        
        return HttpResponse(f"STK Push initiated. Response: {response}")
    
        return redirect("payment_success")
    else:

     return render(request, "payments/initiate_payment.html", {"loop": loop})



"""
============================
 STEP 3: Success Page
============================
"""
def payment_success(request):
    return render(request, "payments/payment_success.html")



"""
============================
 STEP 4: Callback from M-PESA
============================
"""
@csrf_exempt
def mpesa_callback(request):
    data = request.body.decode("utf-8")
    mpesa_data = json.loads(data)

    print("===== MPESA CALLBACK RECEIVED =====")
    print(mpesa_data)

    checkout_id = mpesa_data["Body"]["stkCallback"]["CheckoutRequestID"]
    result_code = mpesa_data["Body"]["stkCallback"]["ResultCode"]

    payment = Payment.objects.filter(checkout_request_id=checkout_id).first()

    if not payment:
        return HttpResponse(status=200)

    if result_code == 0:
        # PAYMENT SUCCESSFUL
        payment.status = "Success"

        # Extract receipt number
        items = mpesa_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        for item in items:
            if item["Name"] == "MpesaReceiptNumber":
                payment.receipt_number = item["Value"]

        payment.save()

        payment.loop.is_purchased_by.add(payment.user)

    else:
        # PAYMENT FAILED
        payment.status = "Failed"
        payment.save()

    return HttpResponse(status=200)
