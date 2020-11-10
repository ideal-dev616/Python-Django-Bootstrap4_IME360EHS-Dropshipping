import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings

from django.core.mail import send_mail
from ime360ehs.models import User, MailBox
from django.db import connection

import pdfkit

# from ime360ehs.services import (
#     getCompanyInfo,
#     getBearerTokenFromRefreshToken,
#     getUserProfile,
#     getBearerToken,
#     getSecretKey,
#     validateJWTToken,
#     revokeToken,
# )

# from intuitlib.client import AuthClient
# from intuitlib.enums import Scopes

global_accessToken = ""
global_refreshToken = ""
global_realmId = ""

curURL = ""

# def accessAPI(request):
#     global curURL
#     curURL = request.POST.get('curURL', None)

#     auth_client = AuthClient(
#         settings.CLIENT_ID, 
#         settings.CLIENT_SECRET, 
#         settings.REDIRECT_URI, 
#         settings.ENVIRONMENT, 
#         state_token=request.session.get('state', None),
#     )

#     url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

#     return JsonResponse({'result':url})

# def callback(request):
#     auth_code = request.GET.get('code', None)
#     realmId = request.GET.get('realmId', None)

#     if auth_code is None:
#         return HttpResponseBadRequest()
#     else: 
#         try:
#             bearer = getBearerToken(auth_code)
#         except:
#             print("Except for getBearerToken!")

#     global global_accessToken
#     global global_refreshToken
#     global global_realmId
    
#     global_accessToken = bearer.accessToken
#     global_refreshToken = bearer.refreshToken
#     global_realmId = realmId

#     if curURL is None:
#         return HttpResponse("QBO Sync Failed!")
#     else:
#         return redirect(curURL)

# def refreshTokenCall(request):
#     if global_refreshToken != "":
#         bearer = getBearerTokenFromRefreshToken(global_refreshToken)

#         listOfGlobals = globals()
#         listOfGlobals['global_accessToken'] = bearer.accessToken
#         listOfGlobals['global_refreshToken'] = bearer.refreshToken

# def createInvoiceToQBO(request):
#     if global_accessToken != "":
#         url = "https://sandbox-quickbooks.api.intuit.com/v3/company/" + str(global_realmId) + "/invoice?minorversion=51"

#         payload = "{\n  \"Line\": [\n    {\n      \"Amount\": 100.00,\n      \"DetailType\": \"SalesItemLineDetail\",\n      \"SalesItemLineDetail\": {\n        \"ItemRef\": {\n          \"value\": \"1\",\n          \"name\": \"Services\"\n        }\n      }\n    }\n  ],\n  \"CustomerRef\": {\n    \"value\": \"1\"\n  }\n}"
        
#         headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer ' + str(global_accessToken),
#         }

#         response = requests.request("POST", url, headers=headers, data = payload)

#         if response.status_code == 200:
#             return JsonResponse({'result': 'success'})
#         elif response.status_code == 401:
#             refreshTokenCall(request)
#             createPO(request)
#             return JsonResponse({'result': 'refresh'})
#         else:
#             return JsonResponse({'result': 'error'})
#     else:
#         return JsonResponse({'result': 'error'})


# def createPO(request):
#     if global_accessToken != "":
#         url = "https://sandbox-quickbooks.api.intuit.com/v3/company/" + str(global_realmId) + "/purchaseorder?minorversion=51"

#         payload = "{\n    \"Line\": [{\n        \"Amount\": 25.0,\n        \"DetailType\": \"ItemBasedExpenseLineDetail\",\n        \"ItemBasedExpenseLineDetail\": {\n            \"CustomerRef\": {\n                \"value\": \"3\",\n                \"name\": \"Beautiful Jackets !!!!!\"\n            },\n            \"BillableStatus\": \"NotBillable\",\n            \"ItemRef\": {\n                \"value\": \"11\",\n                \"name\": \"Pump\"\n            },\n            \"UnitPrice\": 25,\n            \"Qty\": 1,\n            \"TaxCodeRef\": {\n                \"value\": \"NON\"\n            }\n        }\n    }],\n    \"VendorRef\": {\n        \"value\": \"41\",\n        \"name\": \"Hicks Hardware\"\n    },\n    \"APAccountRef\": {\n        \"value\": \"33\",\n        \"name\": \"Accounts Payable (A/P)\"\n    },\n    \"TotalAmt\": 25.0\n}\n"

#         headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer ' + str(global_accessToken),
#         }

#         response = requests.request("POST", url, headers=headers, data = payload)

#         if response.status_code == 200:
#             return JsonResponse({'result': 'success'})
#         elif response.status_code == 401:
#             refreshTokenCall(request)
#             createPO(request)
#             return JsonResponse({'result': 'refresh'})
#         else:
#             return JsonResponse({'result': 'error'})
#     else:
#         print("except")
#         return JsonResponse({'result': 'error'})

def getOrderMails(request):
    result = ""
    notify = "yes"
    try:
        # Save to Mailbox
        userid = request.POST.get('userId')
        news = MailBox.objects.filter(toUser=userid).order_by("-dateTime")
        notifications = news[:10]
        data = ""

        if request.session['notification_length'] == 0:
            notify = "no"
        elif request.session['notification_length'] >= len(news):
            notify = "no"
        else:
            notify = "yes"
        request.session['notification_length'] = len(news)

        for item in notifications:
            data += '<a href="http://127.0.0.1:8000/vieworder/?id='
            data += str(item.orderId)
            data += '"> <div class="btn btn-primary btn-circle"><i class="ti-user"></i></div>'
            data += '<div class="mail-contnet"> <h5>'
            data += str(item.header)
            data += '</h5> <span class="mail-desc">'
            data += str(item.content)
            data += '</span> <span class="time">'
            data += str(item.dateTime)
            data += '</span> </div> </a>'

        result = "success"
    except:
        result = "error"

    return JsonResponse({'result': result, "data": data, "notify":notify})

def sendScheduledAlert(request):
    result = "success"
    try:
        query = """SELECT a.id, a.intakeAgent, a.doctorId, a.locationId, a.alertStatus, b.clinic, b.location 
                FROM tbl_scheduledtime AS a LEFT JOIN tbl_assesslocation AS b ON a.locationId = b.id 
                WHERE alertStatus = 0 AND (a.scheduledTime >= NOW() - INTERVAL 200 MINUTE AND a.scheduledTime <= NOW());"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            exist = cursor.fetchall()
        emails = []
        for item in exist:
            # Save to Mailbox
            intake = User.objects.filter(id=item[1])[0]
            doctor = User.objects.filter(id=item[2])[0]
            doctor_name = str(doctor.first_name) + ' ' + str(doctor.last_name)
            
            dt = datetime.datetime.now()
            dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
            subject = "IME Alert."
            content = 'A schedule is coming with Doctor ' + str(doctor_name)
            message = content
            
            
            mailItem = MailBox(fromUser=1, toUser=intake.id, mailType="SendScheduledAlertToIntakeAgent", orderId='', header=subject, content=content, dateTime=dateTime)
            mailItem.save()

            emails.append(str(intake.email))

        # Send Order Email to Admins.
        # if emails:
        #     email_from = settings.EMAIL_HOST_USER
        #     recipient_list = emails
        #     send_mail( subject, message, email_from, recipient_list )

        emails = []
        for item in exist:
            print(item)
            # Save to Mailbox
            intake = User.objects.filter(id=item[1])[0]
            doctor = User.objects.filter(id=item[2])[0]
            intake_name = str(intake.first_name) + ' ' + str(intake.last_name)
            
            dt = datetime.datetime.now()
            dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
            subject = "IME Alert."
            content = 'A schedule is coming with Intake Agent ' + str(doctor_name)
            message = content
            
            
            mailItem = MailBox(fromUser=1, toUser=doctor.id, mailType="SendScheduledAlertToDoctor", orderId='', header=subject, content=content, dateTime=dateTime)
            mailItem.save()

            emails.append(str(doctor.email))

        # Send Order Email to Admins.
        # if emails:
        #     email_from = settings.EMAIL_HOST_USER
        #     recipient_list = emails
        #     send_mail( subject, message, email_from, recipient_list )
    except:
        result = "error"
    return JsonResponse({'result': result})