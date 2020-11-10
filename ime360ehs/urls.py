from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls import url

from . import views, apis

urlpatterns = [
    # Page - Main
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('users/', views.users, name='users'),

    path('clinic/', views.clinic, name='clinic'),
    path('clinic/add', views.addClinic, name='addClinic'),
    path('clinic/edit', views.editClinic, name='editClinic'),
    path('product/', views.product, name='product'),
    path('order/create', views.createOrder, name='createOrder'),
    path('orders/', views.orders, name='orders'),
    path('order/view', views.viewOrder, name='viewOrder'),
    path('invoices/', views.invoices, name='invoices'),

    path('assessment/', views.assessments, name='assessments'),
    path('assessment/view', views.assess_view, name='assess_view'),
    path('assessment/manage', views.assess_default, name='assess_default'),
    path('assessment/type', views.assess_type, name='assess_type'),
    path('assessment/location', views.assess_location, name='assess_location'),
    path('question/banklist', views.question_banklist, name='question_banklist'),
    path('referral/agency', views.referral_agency, name='referral_agency'),
    path('scheduler', views.scheduler, name='scheduler'),


    # ---------------------------------- Admin ----------------------------------
    # Page - Authentication
    url(r'^ajax/login/user/$', views.userLogin, name='userLogin'),
    url(r'^ajax/logout/user/$', views.userLogout, name='userLogout'),

    # Page - User Management
    url(r'^ajax/add/user/$', views.addUser, name='addUser'),
    url(r'^ajax/edit/user/$', views.editUser, name='editUser'),
    url(r'^ajax/delete/user/$', views.deleteUser, name='deleteUser'),
    

    # ---------------------------------- EHS ----------------------------------
    # Page - Clinic Management
    url(r'^ajax/add/clinic_user/$', views.addClinicUser, name='addClinicUser'),
    url(r'^ajax/edit/clinic_user/$', views.editClinicUser, name='editClinicUser'),
    url(r'^ajax/delete/clinic/$', views.deleteClinic, name='deleteClinic'),
    url(r'^ajax/cusers_by_cmanager/$', views.cUsersByCManager, name='cUsersByCManager'),
    url(r'^ajax/add/cusers/$', views.addCUsers, name='addCUsers'),

    # Page - Product Management
    url(r'^ajax/add/product/$', views.addProduct, name='addProduct'),
    url(r'^ajax/edit/product/$', views.editProduct, name='editProduct'),
    url(r'^ajax/delete/product/$', views.deleteProduct, name='deleteProduct'),
    
    # Page - Create Order
    url(r'^ajax/submit/order/$', views.submitOrder, name='submitOrder'),
    url(r'^ajax/create/order_template/$', views.createOrderTemplate, name='createOrderTemplate'),
    url(r'^ajax/change/order_template/$', views.changeOrderTemplate, name='changeOrderTemplate'),
    url(r'^ajax/insert/more_products/$', views.insertMoreProducts, name='insertMoreProducts'),
    url(r'^ajax/update/ordersheet/$', views.updateOrdersheet, name='updateOrdersheet'),
    url(r'^ajax/get/more_products/$', views.getMoreProducts, name='getMoreProducts'),

    # Page - View Order
    url(r'^ajax/get/missed_orders/$', views.getMissedOrders, name='getMissedOrders'),
    url(r'^ajax/create/invoice/$', views.createInvoice, name='createInvoice'),
    url(r'^ajax/get/invoice_history/$', views.getInvoiceHistory, name='getInvoiceHistory'),
    url(r'^ajax/save/invoice_status/$', views.saveInvoiceStatus, name='saveInvoiceStatus'),
    url(r'^ajax/repeat/history_order/$', views.repeatHistoryOrder, name='repeatHistoryOrder'),

    # Page - Invoices & Status
    url(r'^ajax/upload/packing_slip/$', views.uploadPackingSlip, name='uploadPackingSlip'),
    url(r'^ajax/delete/packing_slip/$', views.deletePackingSlip, name='deletePackingSlip'),


    # ---------------------------------- IME ----------------------------------
    # Page - Referral Agency
    url(r'^ajax/add_referralagency/$', views.add_referralagency, name='add_referralagency'),
    url(r'^ajax/edit_referralagency/$', views.edit_referralagency, name='edit_referralagency'),
    url(r'^ajax/delete_referralagency/$', views.delete_referralagency, name='delete_referralagency'),

    # Page - Question Bank List
    url(r'^ajax/add_question/$', views.add_question, name='add_question'),
    url(r'^ajax/edit_question/$', views.edit_question, name='edit_question'),
    url(r'^ajax/delete_question/$', views.delete_question, name='delete_question'),

    # Page - Assessment Location
    url(r'^ajax/add_location/$', views.add_location, name='add_location'),
    url(r'^ajax/edit_location/$', views.edit_location, name='edit_location'),
    url(r'^ajax/delete_location/$', views.delete_location, name='delete_location'),

    # Page - Assessment Type
    url(r'^ajax/add_assesstype/$', views.add_assesstype, name='add_assesstype'),
    url(r'^ajax/edit_assesstype/$', views.edit_assesstype, name='edit_assesstype'),
    url(r'^ajax/delete_assesstype/$', views.delete_assesstype, name='delete_assesstype'),

    # Page - Assessment Name
    url(r'^ajax/add_assessmanagename/$', views.add_assessmanagename, name='add_assessmanagename'),
    url(r'^ajax/edit_assessmanagename/$', views.edit_assessmanagename, name='edit_assessmanagename'),
    url(r'^ajax/delete_assessmanagename/$', views.delete_assessmanagename, name='delete_assessmanagename'),

    # Page - Assessment Intake Form
    url(r'^ajax/create_assess/$', views.create_assess, name='create_assess'),

    url(r'^ajax/add_docsummary/$', views.add_docsummary, name='add_docsummary'),
    url(r'^ajax/delete_docsummary/$', views.delete_docsummary, name='delete_docsummary'),
    url(r'^ajax/add_mva/$', views.add_mva, name='add_mva'),
    url(r'^ajax/add_treattodate/$', views.add_treattodate, name='add_treattodate'),
    url(r'^ajax/delete_treat/$', views.delete_treat, name='delete_treat'),
    url(r'^ajax/add_medicalhistory/$', views.add_medicalhistory, name='add_medicalhistory'),
    url(r'^ajax/delete_medicalhistory/$', views.delete_medicalhistory, name='delete_medicalhistory'),
    url(r'^ajax/add_familyhistory/$', views.add_familyhistory, name='add_familyhistory'),
    url(r'^ajax/delete_familyhistory/$', views.delete_familyhistory, name='delete_familyhistory'),
    url(r'^ajax/add_medication/$', views.add_medication, name='add_medication'),
    url(r'^ajax/delete_medication/$', views.delete_medication, name='delete_medication'),
    url(r'^ajax/add_allergy/$', views.add_allergy, name='add_allergy'),
    url(r'^ajax/delete_allergy/$', views.delete_allergy, name='delete_allergy'),
    url(r'^ajax/add_socialhistory/$', views.add_socialhistory, name='add_socialhistory'),
    url(r'^ajax/delete_socialhistory/$', views.delete_socialhistory, name='delete_socialhistory'),
    url(r'^ajax/save_activitytolerance/$', views.save_activitytolerance, name='save_activitytolerance'),
    url(r'^ajax/add_occu/$', views.add_occu, name='add_occu'),
    url(r'^ajax/delete_occu/$', views.delete_occu, name='delete_occu'),
    url(r'^ajax/save_psychological/$', views.save_psychological, name='save_psychological'),
    url(r'^ajax/save_presentcomplaints/$', views.save_presentcomplaints, name='save_presentcomplaints'),
    url(r'^ajax/add_diagnose/$', views.add_diagnose, name='add_diagnose'),
    url(r'^ajax/delete_diagnose/$', views.delete_diagnose, name='delete_diagnose'),
    url(r'^ajax/save_referralquestions/$', views.save_referralquestions, name='save_referralquestions'),
    url(r'^ajax/add_physicalexam/$', views.add_physicalexam, name='add_physicalexam'),


    url(r'^ajax/getOrderMails/$', apis.getOrderMails, name='getOrderMails'),
    url(r'^ajax/sendScheduledAlert/$', apis.sendScheduledAlert, name='sendScheduledAlert'),

    # Page - Scheduler
    url(r'^ajax/saveScheduleSheet/$', views.saveScheduleSheet, name='saveScheduleSheet'),
    url(r'^ajax/getScheduleSheet/$', views.getScheduleSheet, name='getScheduleSheet'),
    url(r'^ajax/requestSchedule/$', views.requestSchedule, name='requestSchedule'),
    url(r'^ajax/sendSchedule/$', views.sendSchedule, name='sendSchedule'),
    url(r'^ajax/saveScheduled/$', views.saveScheduled, name='saveScheduled'),
    url(r'^ajax/getScheduled/$', views.getScheduled, name='getScheduled'),


    # ---------------------------------- QBO APIs ----------------------------------
    # url(r'^ajax/accessAPI/$', apis.accessAPI, name='accessAPI'),
    # url(r'^callback/$', apis.callback, name='callback'),
    # url(r'^ajax/createPO/$', apis.createPO, name='createPO'),
    # url(r'^ajax/createInvoiceToQBO/$', apis.createInvoiceToQBO, name='createInvoiceToQBO'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
