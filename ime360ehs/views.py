from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date
from django.db import connection
from django.http import JsonResponse
from django.conf import settings

from ime360ehs.models import User, Clinic, Product, CustomOrderSheet, Order, OrderedProduct, OrderTemplate, ReferralAgency, QuestionBankList, AssessLocation, AssessManageName, AssessType, ClinicUsers, MailBox, BackOrder, Scheduler, ScheduledTime, Assessment, AssessDocSummary, AssessMVADetails, AssessTreatToDate, AssessPastMedicalHistory, AssessFamilyHistory, AssessMedication, AssessAllergies, AssessSocialHistory, AssessActivityTolerances, AssessOccupantionalStatus, AssessPsychologicalStatus, AssessPresentComplaints, AssessPhysicalExam, AssessDiagnoses, AssessReferralQuestions

import uuid
import json
import os
from django.db.models import Max
import datetime
from datetime import date

from django.core.mail import send_mail
# ---------------------- ADMIN ----------------------

# Page - Authentication & Main
def userLogin(request):
    msg = ''
    username = ''
    userrole = ''
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.status == "true":
                login(request, user)
                username = user.first_name + " " + user.last_name + " "
                request.session['username'] = username
                request.session['userid'] = user.id
                request.session['userrole'] = user.role
                request.session['notification_length'] = 0
                request.session['absoluteRoute'] = "/static"
                userrole = user.role
                msg = 'success'
            else:
                msg = 'inactive'
        else:
            msg = 'invalid'
    except:
        msg = "invalid"
    
    return JsonResponse({'result':msg, 'username':username, 'userrole':userrole})

def userLogout(request):
    logout(request)
    try:
        del request.session['username']
        del request.session['userid']
        del request.session['userrole']
        del request.session['notification_length']
        del request.session['absoluteRoute']
    except:
        pass
    return render(request, 'login.html')

def index(request):
    return render(request, 'login.html')

def dashboard(request):
    if request.session.has_key('username'):
        return render(request, 'dashboard.html')
    else:
        return render(request, 'login.html')


# Page - User Management
@csrf_protect
def addUser(request):
    result = ""
    try:
        role = request.POST.get('role')
        status = request.POST.get('status')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        extension = request.POST.get('extension')
        password = request.POST.get('password')

        lstUsers = User.objects.filter(email=email)
        if len(lstUsers) > 0:
            result = "exist"
        else:
            try:
                myfile = request.FILES['signature']
                filename = myfile._get_name()
                ext = filename[filename.rfind('.'):]
                file_name = str(uuid.uuid4())+ext
                path = '/image/signature/'
                full_path= str(path) + str(file_name)
                fd = open('%s/%s' % (settings.STATICFILES_DIRS[0],str(path) + str(file_name)), 'wb')
                for chunk in myfile.chunks():
                    fd.write(chunk)
                fd.close()
            except:
                full_path = ''

            user = User(role=role, status=status, first_name=firstname, last_name=lastname, email=email, phone=phone, extension=extension, password=password, is_superuser=False)
            user.set_password(user.password)
            user.signature = full_path
            user.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def editUser(request):
    result = ""
    try:
        role = request.POST.get('role')
        status = request.POST.get('status')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        extension = request.POST.get('extension')
        password = request.POST.get('password')

        image_exist = request.POST.get('image_exist')

        user = User.objects.get(email=email)
        path = '/image/signature/'
        
        full_path = ""
        try:
            myfile = request.FILES['signature']
            filename = myfile._get_name()
            ext = filename[filename.rfind('.'):]
            file_name = str(uuid.uuid4())+ext
            path = '/image/signature/'
            full_path= str(path) + str(file_name)
            fd = open('%s/%s' % (settings.STATICFILES_DIRS[0],str(path) + str(file_name)), 'wb')
            for chunk in myfile.chunks():
                fd.write(chunk)
            fd.close()

            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(user.signature))
            except:
                print("remove error")
        except:
            if(image_exist == "block"):
                full_path = user.signature
            else:
                full_path = ''
                try:
                    os.remove(settings.STATICFILES_DIRS[0] + str(user.signature))
                except:
                    print("remove error")

        user.role = role
        user.status = status
        user.first_name = firstname
        user.last_name = lastname
        user.phone = phone
        user.extension = extension
        user.password = password
        user.set_password(user.password)
        user.signature = full_path
        user.save()
        result = "success"
    except:
        result = "error"
    return JsonResponse({'result':result})

def deleteUser(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            user = User.objects.filter(id=id)
            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(user[0].signature))
            except:
                print("remove error")
            user.delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})

def users(request):
    if request.session.has_key('username'):
        return render(request, 'users.html', {'users':User.objects.all()})
    else:
        return render(request, 'login.html')

def cUsersByCManager(request):
    cmanager = request.POST.get("cmanager")

    query = "SELECT a.id, a.first_name, a.last_name, b.cmanager FROM (SELECT id, first_name, last_name FROM tbl_users WHERE role = 'Clinic User') AS a LEFT JOIN (SELECT * FROM tbl_clinicusers WHERE cmanager = " + cmanager + " OR cmanager IS NULL) AS b ON a.id = b.cuser"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result = "<select multiple id='add_clinicusers' name='add_clinicusers[]'>"
    for row in rows:
        if row[3] is None:
            result += "<option value=" + str(row[0]) + ">" + str(row[1]) + " " + str(row[2]) + "</option>"
        else:
            result += "<option value=" + str(row[0]) + " selected>" + str(row[1]) + " " + str(row[2]) + "</option>"
    result += "</select>"

    return JsonResponse({'result':result})

def addCUsers(request):
    cmanager = request.POST.get("cmanager")
    cusers = request.POST.get("cusers").split(",")

    try:
        d = ClinicUsers.objects.filter(cmanager=cmanager).delete()
        d.execute()
    except:
        print("nothing exists")

    for cuser in cusers:
        row = ClinicUsers(cmanager=cmanager, cuser=cuser)
        row.save()

    return JsonResponse({'result':"success"})


# ---------------------- EHS ----------------------

# Page - Clinic Management
def clinic(request):
    if request.session.has_key('username'):
        return render(request, 'clinic.html', {'clinics':Clinic.objects.all(), "currentusernameUser":request.session['username']})
    else:
        return render(request, 'login.html')

def addClinic(request):
    if request.session.has_key('username'):        
        data = User.objects.filter(role="Clinic User")
        return render(request, 'addclinic.html', {'clinic_users': data})
    else:
        return render(request, 'login.html')

def editClinic(request):
    if request.session.has_key('username'):
        clinic_id = request.GET['id']
        currentUser = Clinic.objects.filter(id=clinic_id)[0]
        data = User.objects.filter(role="Clinic User")

        return render(request, 'editclinic.html', {'clinic_users': data, 'currentUser': currentUser})
    else:
        return render(request, 'login.html')

def addClinicUser(request):
    result = ""
    try:
        clinic = request.POST.get('clinic')
        motto = request.POST.get('motto')
        website = request.POST.get('website')
        shippingcost = request.POST.get('shippingcost')
        note = request.POST.get('note')

        addresstype = request.POST.get('addresstype')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        region = request.POST.get('region')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        clinicusers = request.POST.get('clinicusers')

        existUser = Clinic.objects.filter(clinic_name=clinic)
        if len(existUser) > 0:
            result = "exist"
        else:
            clinic = Clinic(clinic_name=clinic, motto_name=motto, website=website, 
                            ship_cost=shippingcost, note_profile=note, address_type=addresstype, 
                            address_line1=address1, address_line2=address2, country=country, 
                            region=region, city=city, postal_code=postcode, clinic_users=clinicusers)
            clinic.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def editClinicUser(request):
    result = ""
    try:
        user_id = request.POST.get('id')
        clinic = request.POST.get('clinic')
        motto = request.POST.get('motto')
        website = request.POST.get('website')
        shippingcost = request.POST.get('shippingcost')
        note = request.POST.get('note')

        addresstype = request.POST.get('addresstype')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        region = request.POST.get('region')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        clinicusers = request.POST.get('clinicusers')

        user = Clinic.objects.filter(id=user_id)[0]
        user.clinic_name=clinic
        user.motto_name=motto
        user.website=website
        user.ship_cost=shippingcost
        user.note_profile=note
        user.address_type=addresstype
        user.address_line1=address1
        user.address_line2=address2
        user.country=country
        user.region=region
        user.city=city
        user.postal_code=postcode
        user.clinic_users=clinicusers
        user.save()
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def deleteClinic(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            Clinic.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})
  

# Page - Product Management
def product(request):
    if request.session.has_key('username'):
        return render(request, 'product.html', {'products':Product.objects.all()})
    else:
        return render(request, 'login.html')

def addProduct(request):
    result = ""
    try:
        segment = request.POST.get('segment')
        code = request.POST.get('code')
        unit = request.POST.get('unit')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        manufacturer = request.POST.get('manufacturer')
        markup = request.POST.get('markup')
        category = request.POST.get('category')
        retail = request.POST.get('retail')
        status = request.POST.get('status')
        product_type = request.POST.get('type')
        service_cost = request.POST.get('service_cost')
        service_markup = request.POST.get('service_markup')
        service_retail = request.POST.get('service_retail')

        lstProduct = Product.objects.filter(description=description)
        if len(lstProduct) > 0:
            result = "exist"
        else:
            try:
                myfile = request.FILES['img_product']
                filename = myfile._get_name()
                ext = filename[filename.rfind('.'):]
                file_name = str(uuid.uuid4())+ext
                path = '/image/product/'
                full_path= str(path) + str(file_name)
                fd = open('%s/%s' % (settings.STATICFILES_DIRS[0],str(path) + str(file_name)), 'wb')
                for chunk in myfile.chunks():
                    fd.write(chunk)
                fd.close()
            except:
                full_path = ''

            product = Product(segment=segment, product_code=code, unit=unit, description=description, cost=cost, manufacturer=manufacturer, 
                            markup=markup, category=category, retail=retail, status=status, product_type=product_type, 
                            service_cost=service_cost, service_markup=service_markup, service_retail=service_retail)
            product.product_image = full_path
            product.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def editProduct(request):
    result = ""
    try:
        id = request.POST.get('id')
        segment = request.POST.get('segment')
        code = request.POST.get('code')
        unit = request.POST.get('unit')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        manufacturer = request.POST.get('manufacturer')
        markup = request.POST.get('markup')
        category = request.POST.get('category')
        retail = request.POST.get('retail')
        status = request.POST.get('status')
        product_type = request.POST.get('type')
        service_cost = request.POST.get('service_cost')
        service_markup = request.POST.get('service_markup')
        service_retail = request.POST.get('service_retail')

        image_exist = request.POST.get('image_exist')

        product = Product.objects.filter(id=id)[0]
        path = '/image/product/'
        
        full_path = ""
        try:
            myfile = request.FILES['img_product']
            filename = myfile._get_name()
            ext = filename[filename.rfind('.'):]
            file_name = str(uuid.uuid4())+ext
            full_path= str(path) + str(file_name)
            fd = open('%s/%s' % (settings.STATICFILES_DIRS[0],str(path) + str(file_name)), 'wb')
            for chunk in myfile.chunks():
                fd.write(chunk)
            fd.close()

            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(product.product_image))
            except:
                print("remove error")
            
        except:
            if(image_exist == "block"):
                full_path = product.product_image
            else:
                full_path = ''
                try:
                    os.remove(settings.STATICFILES_DIRS[0] + str(product.product_image))
                except:
                    print("remove error")

        product.segment = segment 
        product.product_code = code
        product.unit = unit
        product.description = description
        product.cost = cost
        product.manufacturer = manufacturer
        product.markup = markup
        product.category = category
        product.retail = retail
        product.status = status
        product.product_type = product_type
        product.service_cost = service_cost
        product.service_markup = service_markup
        product.service_retail = service_retail
        product.product_image = full_path
        product.save()
        result = "success"
    except:
        result = "error"
    return JsonResponse({'result':result})

def deleteProduct(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            product = Product.objects.filter(id=id)
            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(product[0].product_image))
            except:
                print("remove error")
            product.delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})
     

# Page - View Order
def orders(request):
    query1 = ""
    if request.session.has_key('username'):
        if request.session['userrole'] == "Clinic User":
            query = """SELECT * FROM (SELECT k.id, k.clinic_name, k.order_date, k.po_number, k.total, IFNULL(k.sum_invoiced, 0), IFNULL(k.count_paid, 0), IFNULL(l.count_notsent,0), IFNULL(k.count_paid, 0) + IFNULL(l.count_notsent,0), k.clinic_id, k.user_id, k.order_note 
            FROM (SELECT i.id, i.clinic_id, i.user_id, i.po_number, i.order_date, i.order_note, i.clinic_name, i.total, i.sum_invoiced, j.count_paid 
            FROM (SELECT * FROM (SELECT * FROM (
            SELECT e.id, e.clinic_id, e.user_id, e.po_number, e.order_date, e.order_note, f.clinic_name 
            FROM tbl_orders AS e 
            LEFT JOIN tbl_clinics AS f ON e.clinic_id = f.id) AS c 
            LEFT JOIN (SELECT a.order_id, ROUND(SUM(a.qty * b.retail), 2) AS total 
            FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id GROUP BY order_id) AS d ON c.id = d.order_id) AS g
            LEFT JOIN (SELECT orderId, SUM(invoiced) AS sum_invoiced FROM tbl_backorder GROUP BY orderId) AS h ON g.id = h.orderId) AS i
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_paid FROM tbl_backorder WHERE payment="Paid" GROUP BY orderId) AS j ON i.id = j.orderId) AS k 
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_notsent FROM tbl_backorder WHERE payment="Not Sent" GROUP BY orderId) AS l ON k.id = l.orderId) AS m
            LEFT JOIN (SELECT order_id, SUM(qty) FROM tbl_orderedproduct GROUP BY order_id) AS n ON m.id = n.order_id WHERE m.user_id = """ + str(request.session['userid']) + """  ORDER BY m.id DESC"""
        elif request.session['userrole'] == "Clinic Manager":
            query = """SELECT o.id, o.clinic_name, o.order_date, o.po_number, o.total, IFNULL(o.sum_invoiced, 0), IFNULL(o.count_paid, 0), IFNULL(o.count_notsent,0), IFNULL(o.count_paid, 0) + IFNULL(o.count_notsent,0), o.clinic_id, o.cuser, o.order_note, p.order_id, p.qty  FROM (
            SELECT m.id, m.clinic_name, m.order_date, m.po_number, m.total, m.order_note, m.clinic_id, m.cmanager, m.cuser, m.sum_invoiced, m.count_paid, n.count_notsent  FROM (
            SELECT k.id, k.clinic_name, k.order_date, k.po_number, k.total, k.order_note, k.clinic_id, k.cmanager, k.cuser, k.sum_invoiced, l.count_paid  FROM (
            SELECT i.id, i.clinic_name, i.order_date, i.po_number, i.total, i.order_note, i.clinic_id, i.cmanager, i.cuser, j.sum_invoiced  FROM (
            SELECT * FROM (
            SELECT * FROM (
            SELECT e.id, e.clinic_id, e.user_id, e.po_number, e.order_date, e.order_note, f.clinic_name FROM 
            tbl_orders AS e LEFT JOIN tbl_clinics AS f ON e.clinic_id = f.id) AS c 
            LEFT JOIN (SELECT a.order_id, ROUND(SUM(a.qty * b.retail), 2) AS total FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id GROUP BY order_id) AS d 
            ON c.id = d.order_id) AS g RIGHT JOIN (SELECT cmanager, cuser FROM tbl_clinicusers WHERE cmanager = """ + str(request.session['userid']) + """) AS h ON g.user_id = h.cuser WHERE g.order_id IS NOT NULL ) AS i
            LEFT JOIN (SELECT orderId, SUM(invoiced) AS sum_invoiced FROM tbl_backorder GROUP BY orderId) AS j ON i.id = j.orderId) AS k
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_paid FROM tbl_backorder WHERE payment="Paid" GROUP BY orderId) AS l ON k.id = l.orderId) AS m
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_notsent FROM tbl_backorder WHERE payment="Not Sent" GROUP BY orderId) AS n ON m.id = n.orderId) AS o
            LEFT JOIN (SELECT order_id, SUM(qty) AS qty FROM tbl_orderedproduct GROUP BY order_id) AS p ON o.id = p.order_id ORDER BY o.id DESC"""

            query1 = """SELECT * FROM (SELECT k.id, k.clinic_name, k.order_date, k.po_number, k.total, IFNULL(k.sum_invoiced, 0), IFNULL(k.count_paid, 0), IFNULL(l.count_notsent,0), IFNULL(k.count_paid, 0) + IFNULL(l.count_notsent,0), k.clinic_id, k.user_id, k.order_note 
            FROM (SELECT i.id, i.clinic_id, i.user_id, i.po_number, i.order_date, i.order_note, i.clinic_name, i.total, i.sum_invoiced, j.count_paid 
            FROM (SELECT * FROM (SELECT * FROM (
            SELECT e.id, e.clinic_id, e.user_id, e.po_number, e.order_date, e.order_note, f.clinic_name 
            FROM tbl_orders AS e 
            LEFT JOIN tbl_clinics AS f ON e.clinic_id = f.id) AS c 
            LEFT JOIN (SELECT a.order_id, ROUND(SUM(a.qty * b.retail), 2) AS total 
            FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id GROUP BY order_id) AS d ON c.id = d.order_id) AS g
            LEFT JOIN (SELECT orderId, SUM(invoiced) AS sum_invoiced FROM tbl_backorder GROUP BY orderId) AS h ON g.id = h.orderId) AS i
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_paid FROM tbl_backorder WHERE payment="Paid" GROUP BY orderId) AS j ON i.id = j.orderId) AS k 
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_notsent FROM tbl_backorder WHERE payment="Not Sent" GROUP BY orderId) AS l ON k.id = l.orderId) AS m
            LEFT JOIN (SELECT order_id, SUM(qty) FROM tbl_orderedproduct GROUP BY order_id) AS n ON m.id = n.order_id WHERE m.user_id = """ + str(request.session['userid']) + """  ORDER BY m.id DESC"""
        elif request.session['userrole'] == "System Admin" or request.session['userrole'] == "Supplier":
            query = """SELECT * FROM (SELECT k.id, k.clinic_name, k.order_date, k.po_number, k.total, IFNULL(k.sum_invoiced, 0), IFNULL(k.count_paid, 0), IFNULL(l.count_notsent,0), IFNULL(k.count_paid, 0) + IFNULL(l.count_notsent,0), k.clinic_id, k.user_id, k.order_note 
            FROM (SELECT i.id, i.clinic_id, i.user_id, i.po_number, i.order_date, i.order_note, i.clinic_name, i.total, i.sum_invoiced, j.count_paid 
            FROM (SELECT * FROM (SELECT * FROM (
            SELECT e.id, e.clinic_id, e.user_id, e.po_number, e.order_date, e.order_note, f.clinic_name 
            FROM tbl_orders AS e 
            LEFT JOIN tbl_clinics AS f ON e.clinic_id = f.id) AS c 
            LEFT JOIN (SELECT a.order_id, ROUND(SUM(a.qty * b.retail), 2) AS total 
            FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id GROUP BY order_id) AS d ON c.id = d.order_id) AS g
            LEFT JOIN (SELECT orderId, SUM(invoiced) AS sum_invoiced FROM tbl_backorder GROUP BY orderId) AS h ON g.id = h.orderId) AS i
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_paid FROM tbl_backorder WHERE payment="Paid" GROUP BY orderId) AS j ON i.id = j.orderId) AS k 
            LEFT JOIN (SELECT orderId, SUM(invoiceId) AS count_notsent FROM tbl_backorder WHERE payment="Not Sent" GROUP BY orderId) AS l ON k.id = l.orderId) AS m
            LEFT JOIN (SELECT order_id, SUM(qty) FROM tbl_orderedproduct GROUP BY order_id) AS n ON m.id = n.order_id ORDER BY m.id DESC"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            orders = cursor.fetchall()

        if query1 == "":
            orders1 = ""
        else:
            with connection.cursor() as cursor:
                cursor.execute(query1)
                orders1 = cursor.fetchall()

        return render(request, 'orders.html', {'orders':orders, 'orders1':orders1})
    else:
        return render(request, 'login.html')

def viewOrder(request):
    if request.session.has_key('username'):
        request.session['orderid'] = request.GET['id']
        query = "SELECT c.id, c.product_code, c.description, c.unit, c.cost, c.retail, c.qty, IFNULL(FORMAT(c.qty - d.invoiced, 0),0), IFNULL(FORMAT(d.invoiced, 0),0) FROM (SELECT b.id, b.product_code, b.description, b.unit, b.cost, b.retail, a.qty FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id WHERE a.order_id = " + request.session['orderid'] + ") AS c LEFT JOIN (SELECT SUM(invoiced) AS invoiced, productId, orderId FROM tbl_backorder WHERE orderId = " + request.session['orderid'] + " GROUP BY productId) AS d ON c.id = d.productId"
        with connection.cursor() as cursor:
            cursor.execute(query)
            orderedproducts = cursor.fetchall()

        query = "SELECT c.id, c.order_date, c.clinic_name, c.address_line1, c.address_line2, c.country, c.region, d.first_name, d.last_name, d.email, d.phone FROM (SELECT a.id, a.user_id, a.order_date, b.clinic_name, b.address_line1, b.address_line2, b.country, b.region FROM tbl_orders AS a LEFT JOIN tbl_clinics AS b ON a.clinic_id = b.id) AS c LEFT JOIN tbl_users AS d ON c.user_id = d.id WHERE c.id = " + request.session['orderid']
        with connection.cursor() as cursor:
            cursor.execute(query)
            orderdetail = cursor.fetchall()[0]

        query = "SELECT invoiceId, invoiceDate, payment, DATE_ADD(invoiceDate, INTERVAL 30 DAY) FROM tbl_backorder WHERE orderId = " + request.session['orderid'] + " GROUP BY invoiceId ORDER BY id DESC"
        with connection.cursor() as cursor:
            cursor.execute(query)
            backorders = cursor.fetchall()

        return render(request, 'vieworder.html', {'orderedproducts':orderedproducts, "orderdetail":orderdetail, "backorders":backorders})
    else:
        return render(request, 'login.html')

def getMissedOrders(request):
    result = ""
    try:
        query = "SELECT c.id, c.product_code, c.description, c.cost, c.qty, c.order_id, IFNULL(d.invoiced,0) FROM (SELECT b.id, b.product_code, b.description, b.cost, a.qty, a.order_id FROM tbl_orderedproduct AS a LEFT JOIN tbl_products AS b ON a.product_id = b.id WHERE a.order_id = " + request.session['orderid'] + ") AS c LEFT JOIN (SELECT SUM(invoiced) AS invoiced, productId, orderId FROM tbl_backorder WHERE orderId = " + request.session['orderid'] + " GROUP BY productId) AS d ON c.id = d.productId WHERE c.qty - d.invoiced > 0 OR d.invoiced IS NULL"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            products = cursor.fetchall()
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result, 'products': products})

def createInvoice(request):
    result = "success"
    invoiceDate = date.today()
    orderId = request.session['orderid']
    invoiceId = request.POST.get("invoiceId")
    userId = request.POST.get("userId")
    products = request.POST.get("products")
    byemail = request.POST.get("byemail")

    rows = BackOrder.objects.filter(invoiceId=invoiceId)
    if len(rows) > 0:
        result = "exist"
    else:
        for item in json.loads(products):
            row = BackOrder(invoiceDate=invoiceDate, invoiceId=invoiceId, orderId=orderId, productId=item['productId'], invoiced=item['qty'], payment="Not Sent", userId=userId)
            row.save()
    
    max_id = BackOrder.objects.all().aggregate(max_id=Max("id"))['max_id']


    # Save to Mailbox
    admins = User.objects.filter(role="System Admin")
    dt = datetime.datetime.now()
    dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    subject = 'New Shipment has been created.'
    content = 'Please click here to check the Shipment Status.'
    message = 'Please click the link to check the Shipment Status. http://18.221.207.135/vieworder/?id=' + request.session.get("orderid")

    supplier_emails = []
    for supplier in admins:
        mailItem = MailBox(fromUser=userId, toUser=supplier.id, mailType="ProductOrder", orderId=max_id, header=subject, content=content, dateTime=dateTime)
        mailItem.save()

        supplier_emails.append(str(supplier.email))

    supplier_emails.append(byemail)

    # Send Order Email to Suppliers.
    if supplier_emails:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = supplier_emails
        send_mail( subject, message, email_from, recipient_list )
    return JsonResponse({'result':result})

def getInvoiceHistory(request):
    result = ""
    invoiceId = request.POST.get("invoiceId")
    try:
        query = "SELECT e.productId, e.product_code, e.description, e.unit, e.cost, e.retail, e.qty, e.qty - e.invoiced, e.invoiced, e.payment, IFNULL(f.backordered, 0) FROM (SELECT c.productId, c.product_code, c.description, c.unit, c.cost, c.retail, d.qty, c.invoiced, c.payment FROM (SELECT a.invoiceId, a.orderId, a.productId, a.invoiced, a.payment, b.product_code, b.unit, b.description, b.cost, b.retail FROM tbl_backorder AS a LEFT JOIN tbl_products AS b ON a.productId = b.id WHERE a.orderId = " + request.session['orderid'] + " AND invoiceId = '" + invoiceId + "') AS c LEFT JOIN (SELECT order_id, product_id, qty FROM tbl_orderedproduct WHERE order_id = " + request.session['orderid'] + ") AS d ON c.productId = d.product_id) AS e LEFT JOIN (SELECT productId, SUM(invoiced) AS backordered FROM tbl_backorder WHERE orderId = " + request.session['orderid'] + " GROUP BY productId) AS f ON e.productId = f.productId"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            products = cursor.fetchall()

        packingslipURL = BackOrder.objects.filter(invoiceId=invoiceId)[0].packingslipURL
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result, 'products': products, 'packingslipURL' : packingslipURL})


# Page - Create Order
def createOrder(request):
    if request.session.has_key('username'):
        category_condition1 = ""
        category_condition2 = ""
        count_left = 0
        count_right = 0
        category_counts = "SELECT category, COUNT(category) FROM tbl_products GROUP BY category ORDER BY COUNT(category) DESC"
        with connection.cursor() as cursor:
            cursor.execute(category_counts)
            category_counts_arr = cursor.fetchall()
        for category in category_counts_arr:
            if count_left <= count_right:
                if category_condition1 == "":
                    category_condition1 += " category = '" + category[0] + "'"
                else:
                    category_condition1 += " OR category = '" + category[0] + "'"
                count_left += category[1]
            else:
                if category_condition2 == "":
                    category_condition2 += " category = '" + category[0] + "'"
                else:
                    category_condition2 += " OR category = '" + category[0] + "'"
                count_right += category[1]
        
        query = "SELECT id, product_code, category, description FROM tbl_products WHERE"
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition1 + " ORDER BY category")
            ordersheet1 = cursor.fetchall()

        orderData1 = ""
        category1 = ""
        for row in ordersheet1:
            if category1 != str(row[2]).upper():
                category1 = str(row[2]).upper()
                orderData1 += "<tr product-head='" + category1 + "'><td colspan='4'>"+ category1 +"</td></tr>"

            orderData1 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category1 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>
            """
        
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition2 + " ORDER BY category")
            ordersheet2 = cursor.fetchall()

        orderData2 = ""
        category2 = ""
        for row in ordersheet2:
            if category2 != str(row[2]).upper():
                category2 = str(row[2]).upper()
                orderData2 += "<tr product-head='" + category2 + "'><td colspan='4'>"+ category2 +"</td></tr>"
                category2 = str(row[2]).upper()
            orderData2 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category2 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>"""

        return render(request, 'createorder.html', {'products':Product.objects.all(), 'clinics':Clinic.objects.all(), 'order_templates':OrderTemplate.objects.all(), 'orderData1': orderData1, 'orderData2':orderData2})
    else:
        return render(request, 'login.html')

def insertMoreProducts(request):
    result = ""
    orderData1 = ""
    orderData2 = ""
    try:
        updatedIds = request.POST.get('updatedIds')
        template_name = request.POST.get('templateName')

        exist = OrderTemplate.objects.filter(template_name=template_name, user_id=request.session.get('userid')).update(product_id=str(updatedIds))
        
        # Update Order Sheet
        category_condition1 = ""
        category_condition2 = ""
        count_left = 0
        count_right = 0
        query_counts = ""
        if str(request.POST["templateName"]) != "default":
            products_ids = OrderTemplate.objects.filter(template_name=request.POST['templateName'], user_id=request.session.get('userid'))
            print(products_ids)
            for product_id in json.loads(products_ids[0].product_id):
                if query_counts == "":
                    query_counts += " WHERE id = " + product_id
                else:
                    query_counts += " OR id = " + product_id            

        category_counts = "SELECT a.category, COUNT(a.category) FROM (SELECT * FROM tbl_products " + query_counts + ") AS a GROUP BY category ORDER BY COUNT(category) DESC"
        with connection.cursor() as cursor:
            cursor.execute(category_counts)
            category_counts_arr = cursor.fetchall()
        for category in category_counts_arr:
            if count_left <= count_right:
                if category_condition1 == "":
                    category_condition1 += " category = '" + category[0] + "'"
                else:
                    category_condition1 += " OR category = '" + category[0] + "'"
                count_left += category[1]
            else:
                if category_condition2 == "":
                    category_condition2 += " category = '" + category[0] + "'"
                else:
                    category_condition2 += " OR category = '" + category[0] + "'"
                count_right += category[1]
        
        query = "SELECT id, product_code, category, description FROM tbl_products WHERE "
        if str(request.POST["templateName"]) != "default":
            query = "SELECT a.id, a.product_code, a.category, a.description FROM (SELECT * FROM tbl_products " + query_counts + ") AS a WHERE "
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition1 + " ORDER BY category")
            order_sheet1 = cursor.fetchall()

        orderData1 = ""
        category1 = ""
        for row in order_sheet1:
            if category1 != str(row[2]).upper():
                category1 = str(row[2]).upper()
                orderData1 += "<tr product-head='" + category1 + "'><td colspan='4'>"+ category1 +"</td></tr>"

            orderData1 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category1 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>
            """
        
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition2 + " ORDER BY category")
            order_sheet2 = cursor.fetchall()

        orderData2 = ""
        category2 = ""
        for row in order_sheet2:
            if category2 != str(row[2]).upper():
                category2 = str(row[2]).upper()
                orderData2 += "<tr product-head='" + category2 + "'><td colspan='4'>"+ category2 +"</td></tr>"
                category2 = str(row[2]).upper()
            orderData2 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category2 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>"""
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result, 'orderData1':orderData1, 'orderData2':orderData2})

def updateOrdersheet(request):
    category_condition1 = ""
    category_condition2 = ""
    count_left = 0
    count_right = 0
    category_counts = "SELECT category, COUNT(category), id FROM tbl_products as a WHERE " + request.POST["arrCondition"] + " GROUP BY category ORDER BY COUNT(category) DESC"
    with connection.cursor() as cursor:
        cursor.execute(category_counts)
        category_counts_arr = cursor.fetchall()
    for category in category_counts_arr:
        if count_left <= count_right:
            if category_condition1 == "":
                category_condition1 += " category = '" + category[0] + "'"
            else:
                category_condition1 += " OR category = '" + category[0] + "'"
            count_left += category[1]
        else:
            if category_condition2 == "":
                category_condition2 += " category = '" + category[0] + "'"
            else:
                category_condition2 += " OR category = '" + category[0] + "'"
            count_right += category[1]
    
    query = "SELECT id, product_code, category, description FROM tbl_products WHERE"
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (" + query + category_condition1 + " ORDER BY category) AS a WHERE " + request.POST["arrCondition"])
        ordersheet1 = cursor.fetchall()

    orderData1 = ""
    category1 = ""
    for row in ordersheet1:
        if category1 != str(row[2]).upper():
            category1 = str(row[2]).upper()
            orderData1 += "<tr product-head='" + category1 + "'><td colspan='4'>"+ category1 +"</td></tr>"

        orderData1 += """
            <tr id='""" + str(row[0]) + """' product-head='""" + category1 + """'>
                <td>""" + str(row[1]) + """</td>
                <td>""" + str(row[3]) + """</td>
                <td class="touchspin-padding">
                    <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                </td>
                <td style="vertical-align: middle;text-align: center;">
                    <div class="btn-group btn-group-xs" role="group">
                        <button type="button" onclick="deleteproduct(this)" class="btn btn-secondary footable-delete btn_deleteproduct"><span class="fas fa-trash-alt" aria-hidden="true"></span></button>
                    </div>
                </td>
            </tr>
        """
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (" + query + category_condition2 + " ORDER BY category) AS a WHERE " + request.POST["arrCondition"])
        ordersheet2 = cursor.fetchall()

    orderData2 = ""
    category2 = ""
    for row in ordersheet2:
        if category2 != str(row[2]).upper():
            category2 = str(row[2]).upper()
            orderData2 += "<tr product-head='" + category2 + "'><td colspan='4'>"+ category2 +"</td></tr>"
            category2 = str(row[2]).upper()
        orderData2 += """
            <tr id='""" + str(row[0]) + """' product-head='""" + category2 + """'>
                <td>""" + str(row[1]) + """</td>
                <td>""" + str(row[3]) + """</td>
                <td class="touchspin-padding">
                    <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                </td>
                <td style="vertical-align: middle;text-align: center;">
                    <div class="btn-group btn-group-xs" role="group">
                        <button type="button" onclick="deleteproduct(this)" class="btn btn-secondary footable-delete btn_deleteproduct"><span class="fas fa-trash-alt" aria-hidden="true"></span></button>
                    </div>
                </td>
            </tr>"""

    return JsonResponse({'orderData1': orderData1, 'orderData2':orderData2})

def getMoreProducts(request):
    result = ""
    condition = request.POST["condition"]
    try:
        query = "SELECT id, product_code, category, description FROM tbl_products WHERE"
        with connection.cursor() as cursor:
            cursor.execute(query + condition + " ORDER BY category")
            ordersheet = cursor.fetchall()

        orderData = ""
        category = ""
        for row in ordersheet:
            if category != str(row[2]).upper():
                category = str(row[2]).upper()
                orderData += "<tr product-head='" + category + "'><td colspan='4'>"+ category +"</td></tr>"

            orderData += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                </tr>
            """
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result, 'orderData': orderData})

def submitOrder(request):
    result = "success"
    try:
        # Save to Orders
        userid = request.POST.get('userid')
        clinicid = request.POST.get('clinicid')
        ordernote = request.POST.get('ordernote')
        idArr = json.loads(request.POST.get('idArr'))

        order = Order(user_id=userid, clinic_id=clinicid, order_date=date.today(), order_note=ordernote)
        order.save()

        max_id = Order.objects.all().aggregate(max_id=Max("id"))['max_id']

        for product in idArr:
            pro = OrderedProduct(order_id=max_id, product_id=product['product_id'], qty=product['qty'])
            pro.save()

        # Save to Mailbox
        suppliers = User.objects.filter(role="Supplier")

        dt = datetime.datetime.now()
        dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
        subject = 'New Order has been placed.'
        content = 'Please click here to check the order.'
        message = 'Please click the link to check the order. http://18.221.207.135/vieworder/?id=' + str(max_id)
        
        supplier_emails = []
        for supplier in suppliers:
            mailItem = MailBox(fromUser=userid, toUser=supplier.id, mailType="ProductOrder", orderId=max_id, header=subject, content=content, dateTime=dateTime)
            mailItem.save()

            supplier_emails.append(str(supplier.email))

        # Send Order Email to Suppliers.
        if supplier_emails:
            email_from = settings.EMAIL_HOST_USER
            recipient_list = supplier_emails
            send_mail( subject, message, email_from, recipient_list )
        
    except:
        result = "error"

    return JsonResponse({'result':result})

def createOrderTemplate(request):
    result = ""
    user_id = request.session["userid"]
    template_title = request.POST["templateTitle"]
    ids = request.POST["checkedIdArr"]

    exist = OrderTemplate.objects.filter(user_id=user_id, template_name=template_title)
    if exist:
        result = "exist"
    else:
        query = "INSERT INTO tbl_order_template (template_name, product_id, user_id) VALUES ('" + str(template_title) + "', '" + str(ids) + "', '" + str(user_id) + "');"
        connection.cursor().execute(query)
        result = "success"
    return JsonResponse({'result':result})

def changeOrderTemplate(request):
    result = ""
    try:
        category_condition1 = ""
        category_condition2 = ""
        count_left = 0
        count_right = 0
        query_counts = ""
        if str(request.POST["templateTitle"]) != "default":
            products_ids = OrderTemplate.objects.filter(template_name=request.POST['templateTitle'], user_id=request.session.get('userid'))
            print(products_ids)
            for product_id in json.loads(products_ids[0].product_id):
                if query_counts == "":
                    query_counts += " WHERE id = " + product_id
                else:
                    query_counts += " OR id = " + product_id            

        category_counts = "SELECT a.category, COUNT(a.category) FROM (SELECT * FROM tbl_products " + query_counts + ") AS a GROUP BY category ORDER BY COUNT(category) DESC"
        with connection.cursor() as cursor:
            cursor.execute(category_counts)
            category_counts_arr = cursor.fetchall()
        for category in category_counts_arr:
            if count_left <= count_right:
                if category_condition1 == "":
                    category_condition1 += " category = '" + category[0] + "'"
                else:
                    category_condition1 += " OR category = '" + category[0] + "'"
                count_left += category[1]
            else:
                if category_condition2 == "":
                    category_condition2 += " category = '" + category[0] + "'"
                else:
                    category_condition2 += " OR category = '" + category[0] + "'"
                count_right += category[1]
        
        query = "SELECT id, product_code, category, description FROM tbl_products WHERE "
        if str(request.POST["templateTitle"]) != "default":
            query = "SELECT a.id, a.product_code, a.category, a.description FROM (SELECT * FROM tbl_products " + query_counts + ") AS a WHERE "
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition1 + " ORDER BY category")
            order_sheet1 = cursor.fetchall()

        orderData1 = ""
        category1 = ""
        for row in order_sheet1:
            if category1 != str(row[2]).upper():
                category1 = str(row[2]).upper()
                orderData1 += "<tr product-head='" + category1 + "'><td colspan='4'>"+ category1 +"</td></tr>"

            orderData1 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category1 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>
            """
        
        with connection.cursor() as cursor:
            cursor.execute(query + category_condition2 + " ORDER BY category")
            order_sheet2 = cursor.fetchall()

        orderData2 = ""
        category2 = ""
        for row in order_sheet2:
            if category2 != str(row[2]).upper():
                category2 = str(row[2]).upper()
                orderData2 += "<tr product-head='" + category2 + "'><td colspan='4'>"+ category2 +"</td></tr>"
                category2 = str(row[2]).upper()
            orderData2 += """
                <tr id='""" + str(row[0]) + """' product-head='""" + category2 + """'>
                    <td class="ordersheet-action" style="vertical-align: middle;text-align: center;">
                        <input type="checkbox">
                    </td>
                    <td>""" + str(row[1]) + """</td>
                    <td>""" + str(row[3]) + """</td>
                    <td class="touchspin-padding">
                        <input type="number" name="qty_ordered" data-bts-button-down-class="btn btn-secondary btn-outline" data-bts-button-up-class="btn btn-secondary btn-outline">
                    </td>
                </tr>"""
        result = "success"
    except:
        result = "error"
    
    return JsonResponse({'result':result, 'orderData1':orderData1, 'orderData2':orderData2})

# Page - Invoices & Status
def invoices(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "System Admin":
            query = "SELECT invoiceId, invoiceDate, payment, DATE_ADD(invoiceDate, INTERVAL 30 DAY), packingslipURL FROM tbl_backorder GROUP BY invoiceId ORDER BY id DESC"
        
            with connection.cursor() as cursor:
                cursor.execute(query)
                invoices = cursor.fetchall()
            return render(request, 'invoices.html', {'invoices':invoices})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def saveInvoiceStatus(request):
    result = "success"
    idArr = json.loads(request.POST.get('idArr'))

    try:
        for border in idArr:
            query = 'UPDATE tbl_backorder SET payment = "' + str(border["paymentStatus"]) + '" WHERE invoiceId = "' + str(border["invoiceId"]) + '"'
            connection.cursor().execute(query)
    except:
        result = "error"
    return JsonResponse({'result':result})

def repeatHistoryOrder(request):
    result = "success"
    try:
        # Save to Orders
        userid = request.session['userid']
        idArr = json.loads(request.POST.get("idArr"))

        lastorder = Order.objects.filter(id=request.session.get("orderid"))[0]

        order = Order(user_id=userid, clinic_id=lastorder.clinic_id, order_date=date.today(), order_note=lastorder.order_note)
        order.save()

        max_id = Order.objects.all().aggregate(max_id=Max("id"))['max_id']

        for product in idArr:
            pro = OrderedProduct(order_id=max_id, product_id=product['productId'], qty=product['qty'])
            pro.save()

        # Save to Mailbox
        suppliers = User.objects.filter(role="Supplier")

        dt = datetime.datetime.now()
        dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
        subject = 'New Order has been placed.'
        content = 'Please click here to check the order.'
        message = 'Please click the link to check the order. http://18.221.207.135/vieworder/?id=' + str(max_id)
        
        supplier_emails = []
        for supplier in suppliers:
            mailItem = MailBox(fromUser=userid, toUser=supplier.id, mailType="ProductOrder", orderId=max_id, header=subject, content=content, dateTime=dateTime)
            mailItem.save()

            supplier_emails.append(str(supplier.email))

        # Send Order Email to Suppliers.
        if supplier_emails:
            email_from = settings.EMAIL_HOST_USER
            recipient_list = supplier_emails
            send_mail( subject, message, email_from, recipient_list )
        
    except:
        result = "error"

    return JsonResponse({'result':result})

def uploadPackingSlip(request):
    result = ""
    try:
        id = request.POST.get('backorderId')

        border = BackOrder.objects.filter(invoiceId=id)
        path = '/image/packingslip/'
        
        full_path = ""
        try:
            myfile = request.FILES['file_packingslip']
            filename = myfile._get_name()
            ext = filename[filename.rfind('.'):]
            file_name = str(uuid.uuid4())+ext
            full_path= str(path) + str(file_name)
            fd = open('%s/%s' % (settings.STATICFILES_DIRS[0],str(path) + str(file_name)), 'wb')
            for chunk in myfile.chunks():
                fd.write(chunk)
            fd.close()

            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(border.packingslipURL))
            except:
                print("remove error")
            
        except:
            full_path = ''
            try:
                os.remove(settings.STATICFILES_DIRS[0] + str(border.packingslipURL))
            except:
                print("remove error")
        
        for row in border:
            row.packingslipURL = full_path
            row.save()
        result = "success"
    except:
        result = "error"
    return JsonResponse({'result':result})

def deletePackingSlip(request):
    result = ""
    try:
        id = request.POST.get('backorderId')

        border = BackOrder.objects.filter(invoiceId=id)
        
        for row in border:
            row.packingslipURL = ""
            row.save()
        result = "success"
    except:
        result = "error"
    return JsonResponse({'result':result})


# ---------------------- IME ----------------------

def assessments(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            query = """
                    SELECT a.id, a.claimant_lname, a.claimant_fname, b.name, c.first_name, c.last_name, d.first_name, d.last_name, e.clinic, TIMESTAMP(a.date)
                    FROM tbl_assessment AS a 
                    LEFT JOIN tbl_referralagency AS b ON a.referral_agency = b.id 
                    LEFT JOIN tbl_users AS c ON a.physician = c.id 
                    LEFT JOIN tbl_users AS d ON a.intake_agent = d.id
                    LEFT JOIN tbl_assesslocation AS e ON a.location = e.id
                    """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessments = cursor.fetchall()

            return render(request, 'assessments.html', {
                'assessments':assessments,
                'doctors':User.objects.filter(role="Doctor"), 
                'agents':User.objects.filter(role="Intake Agent"),
                'locations':AssessLocation.objects.all(),
                'ragencies':ReferralAgency.objects.all(),
                'types':AssessType.objects.all()
            })
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def assess_view(request):
    assessId = request.GET['assessId']
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            query = """
            SELECT a.id, a.name, a.date, a.amount, a.description, a.disputed, a.diagnostic_exam, b.first_name, b.last_name
            FROM tbl_assessdocsummary AS a
            LEFT JOIN tbl_users AS b
            ON a.physician = b.id
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessdocsummaries = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assesstreattodate
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assesstreat = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assesspastmedicalhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessmedicalhistory = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assessfamilyhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessfamilyhistory = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assessmedication
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessmedication = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assessallergies
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessallergies = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assesssocialhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assesssocialhistory = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assessoccupantionalstatus
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessoccu = cursor.fetchall()

            query = """
            SELECT *
            FROM tbl_assessdiagnoses
            WHERE assess_id = '""" + str(assessId) + """'
            """
            with connection.cursor() as cursor:
                cursor.execute(query)
                assessdiagnose = cursor.fetchall()

            return render(request, 'viewassessment.html', {
                'assessment':Assessment.objects.filter(id=assessId),
                'doctors':User.objects.filter(role="Doctor"), 
                'agents':User.objects.filter(role="Intake Agent"),
                'locations':AssessLocation.objects.all(),
                'ragencies':ReferralAgency.objects.all(),
                'types':AssessType.objects.all(),
                'assessdocsummaries':assessdocsummaries,
                'assessmva':AssessMVADetails.objects.filter(assess_id=assessId),
                'assesstreat':assesstreat,
                'assessmedicalhistory':assessmedicalhistory,
                'assessfamilyhistory':assessfamilyhistory,
                'assessmedication':assessmedication,
                'assessallergies':assessallergies,
                'assesssocialhistory':assesssocialhistory,
                'assessat':AssessActivityTolerances.objects.filter(assess_id=assessId),
                'assessoccu':assessoccu,
                'assesspsychological':AssessPsychologicalStatus.objects.filter(assess_id=assessId),
                'assesspresentcomplaint':AssessPresentComplaints.objects.filter(assess_id=assessId),
                'assessdiagnose':assessdiagnose,
                'assessreferralquestions':AssessReferralQuestions.objects.filter(assess_id=assessId),
                'assessphysicalexam':AssessPhysicalExam.objects.filter(assess_id=assessId),
            })
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def assess_default(request):
    if request.session.has_key('username'):
        return render(request, 'assess_default.html', {'AssessManageName':AssessManageName.objects.all()})
    else:
        return render(request, 'login.html')

def add_assessmanagename(request):
    result = "success"
    try:
        name = request.POST.get('add_name')
        description = request.POST.get('add_value')

        existUser = AssessManageName.objects.filter(name=name)
        if len(existUser) > 0:
            result = "exist"
        else:
            row = AssessManageName(name=name, description=description)
            row.save()
    except:
        result = "error"

    return JsonResponse({'result':result})

def edit_assessmanagename(request):
    result = "success"
    try:
        edit_id = request.POST.get('edit_id')
        name = request.POST.get('edit_name')
        description = request.POST.get('edit_value')

        existUser = AssessManageName.objects.filter(name=name).exclude(id=edit_id)
        if len(existUser) > 0:
            result = "exist"
        else:
            row = AssessManageName.objects.filter(id=edit_id)[0]
            row.name = name
            row.description = description
            row.save()
    except:
        result = "error"

    return JsonResponse({'result':result})

def delete_assessmanagename(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            AssessManageName.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})

def create_assess(request):
    try:
        assessId = request.POST['assessId']
    except:
        assessId = "none"
    result = "success"

    referral_agency = request.POST.get('referral_agency')
    assess_date = request.POST.get('assess_date')
    assess_type = request.POST.get('assess_type')
    insurance_company = request.POST.get('insurance_company')
    date_loss = request.POST.get('date_loss')
    name_mr = request.POST.get('name_mr')
    name_first = request.POST.get('name_first')
    name_last = request.POST.get('name_last')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    claim_no = request.POST.get('claim_no')
    physician = request.POST.get('physician')
    intake_agent = request.POST.get('intake_agent')
    assess_location = request.POST.get('assess_location')
    assess_duration = request.POST.get('assess_duration')
    interpreter = request.POST.get('interpreter')

    if assessId == "none":
        try:
            row = Assessment(referral_agency=referral_agency, date=assess_date, assess_type=assess_type, insurance_company=insurance_company, date_of_loss=date_loss, claimant_mr=name_mr, claimant_fname=name_first, claimant_lname=name_last, birthday=birthday, gender=gender, claim_no=claim_no, physician=physician, intake_agent=intake_agent, location=assess_location, duration=assess_duration, interpreter=interpreter)
            row.save()
        except:
            result = "error"
    else:
        try:
            exist = Assessment.objects.filter(id=assessId)[0]
            exist.referral_agency = referral_agency
            exist.date = assess_date
            exist.assess_type = assess_type
            exist.insurance_company = insurance_company
            exist.date_of_loss = date_loss
            exist.claimant_mr = name_mr
            exist.claimant_fname = name_first
            exist.claimant_lname = name_last
            exist.birthday = birthday
            exist.gender = gender
            exist.claim_no = claim_no
            exist.physician = physician
            exist.intake_agent = intake_agent
            exist.location = assess_location
            exist.duration = assess_duration
            exist.interpreter = interpreter
            exist.save()
        except:
            result = "error"

    return JsonResponse({'result':result})

def add_docsummary(request):
    result = "success"

    assessId = request.POST['assessId']
    name = request.POST.get('name')
    physician = request.POST.get('physician')
    date = request.POST.get('date')
    amount = request.POST.get('amount')
    description = request.POST.get('description')
    disputed = request.POST.get('disputed')
    diagnosticexam = request.POST.get('diagnosticexam')

    try:
        row = AssessDocSummary(assess_id=assessId, name=name, physician=physician, date=date, amount=amount, description=description, disputed=disputed, diagnostic_exam=diagnosticexam)
        row.save()
    except:
        result = "error"

    query = """
            SELECT a.id, a.name, a.date, a.amount, a.description, a.disputed, a.diagnostic_exam, b.first_name, b.last_name
            FROM tbl_assessdocsummary AS a
            LEFT JOIN tbl_users AS b
            ON a.physician = b.id
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        assess_summaries = cursor.fetchall()

    return JsonResponse({'result':result, 'assess_summaries':assess_summaries})

def delete_docsummary(request):
    result = "success"

    assessId = request.POST['assessId']
    summaryid = request.POST.get('summaryid')

    try:
        row = AssessDocSummary.objects.filter(assess_id=assessId, id=summaryid)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT a.id, a.name, a.date, a.amount, a.description, a.disputed, a.diagnostic_exam, b.first_name, b.last_name
            FROM tbl_assessdocsummary AS a
            LEFT JOIN tbl_users AS b
            ON a.physician = b.id
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        assessdocsummaries = cursor.fetchall()

    return JsonResponse({'result':result, 'assess_summaries':assessdocsummaries})

def add_mva(request):
    assessId = request.POST['assessId']
    result = "success"

    id_type = request.POST.get('id_type')
    pos_vehicle = request.POST.get('pos_vehicle')
    num_occupants = request.POST.get('num_occupants')
    accident_location = request.POST.get('accident_location')
    accident_description = request.POST.get('accident_description')
    seatbelt = request.POST.get('seatbelt')
    airbags = request.POST.get('airbags')
    head_injury = request.POST.get('head_injury')
    conscious_loss = request.POST.get('conscious_loss')
    bodily_impact = request.POST.get('bodily_impact')
    exit_vehicle = request.POST.get('exit_vehicle')
    responding_units = request.POST.get('responding_units')
    towed = request.POST.get('towed')
    damage_detail_known = request.POST.get('damage_detail_known')
    damage_to_vehicle = request.POST.get('damage_to_vehicle')
    vehicle_make = request.POST.get('vehicle_make')
    vehicle_model = request.POST.get('vehicle_model')
    vehicle_year = request.POST.get('vehicle_year')
    hospital_visit = request.POST.get('hospital_visit')
    hospital_name = request.POST.get('hospital_name')
    doctor_name = request.POST.get('doctor_name')
    num_days_after = request.POST.get('num_days_after')
    see_family_doctor = request.POST.get('see_family_doctor')
    xray_taken = request.POST.get('xray_taken')
    first_facility_visited = request.POST.get('first_facility_visited')
    other_info = request.POST.get('other_info')

    exist = AssessMVADetails.objects.filter(assess_id=assessId)
    if len(exist) <= 0:
        try:
            row = AssessMVADetails(assess_id=assessId, id_type=id_type, pos_vehicle=pos_vehicle, num_occupants=num_occupants, accident_location=accident_location, accident_description=accident_description, seatbelt=seatbelt, airbags=airbags, head_injury=head_injury, conscious_loss=conscious_loss, bodily_impact=bodily_impact, exit_vehicle=exit_vehicle, responding_units=responding_units, towed=towed, damage_detail_known=damage_detail_known, damage_to_vehicle=damage_to_vehicle, vehicle_make=vehicle_make, vehicle_model=vehicle_model, vehicle_year=vehicle_year, hospital_visit=hospital_visit, hospital_name=hospital_name, doctor_name=doctor_name, num_days_after=num_days_after, see_family_doctor=see_family_doctor, xray_taken=xray_taken, first_facility_visited=first_facility_visited, other_info=other_info)
            row.save()
        except:
            result = "error"
    else:
        try:
            exist[0].id_type = id_type
            exist[0].pos_vehicle = pos_vehicle
            exist[0].num_occupants = num_occupants
            exist[0].accident_location = accident_location
            exist[0].accident_description = accident_description
            exist[0].seatbelt = seatbelt
            exist[0].airbags = airbags
            exist[0].head_injury = head_injury
            exist[0].conscious_loss = conscious_loss
            exist[0].bodily_impact = bodily_impact
            exist[0].exit_vehicle = exit_vehicle
            exist[0].responding_units = responding_units
            exist[0].towed = towed
            exist[0].damage_detail_known = damage_detail_known
            exist[0].damage_to_vehicle = damage_to_vehicle
            exist[0].vehicle_make = vehicle_make
            exist[0].vehicle_model = vehicle_model
            exist[0].vehicle_year = vehicle_year
            exist[0].hospital_visit = hospital_visit
            exist[0].hospital_name = hospital_name
            exist[0].doctor_name = doctor_name
            exist[0].num_days_after = num_days_after
            exist[0].see_family_doctor = see_family_doctor
            exist[0].xray_taken = xray_taken
            exist[0].first_facility_visited = first_facility_visited
            exist[0].other_info = other_info
            exist[0].save()
        except:
            result = "error"

    return JsonResponse({'result':result})

def add_treattodate(request):
    result = "success"

    assessId = request.POST['assessId']
    doctor = request.POST.get('doctor')
    rehab_facility = request.POST.get('rehab_facility')
    address_country = request.POST.get('address_country')
    address_street = request.POST.get('address_street')
    address_city = request.POST.get('address_city')
    address_province = request.POST.get('address_province')
    address_postal = request.POST.get('address_postal')
    frequency_visits = request.POST.get('frequency_visits')
    treat_duration = request.POST.get('treat_duration')
    treat_type = request.POST.get('treat_type')
    date_fvisit = request.POST.get('date_fvisit')
    date_lvisit = request.POST.get('date_lvisit')
    attending_status = request.POST.get('attending_status')

    try:
        row = AssessTreatToDate(assess_id=assessId, doctor=doctor, rehab_facility=rehab_facility, address_country=address_country, address_street=address_street, address_city=address_city, address_province=address_province, address_postal=address_postal, frequency_visits=frequency_visits, treat_duration=treat_duration, treat_type=treat_type, date_fvisit=date_fvisit, date_lvisit=date_lvisit, attending_status=attending_status)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesstreattodate
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_treat(request):
    result = "success"

    assessId = request.POST['assessId']
    treatid = request.POST.get('treatid')

    try:
        row = AssessTreatToDate.objects.filter(assess_id=assessId, id=treatid)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesstreattodate
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def add_medicalhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    surgical_history = request.POST.get('surgical_history')
    hospitalization = request.POST.get('hospitalization')
    current_illness = request.POST.get('current_illness')
    prev_accident_history = request.POST.get('prev_accident_history')
    date = request.POST.get('date')

    try:
        row = AssessPastMedicalHistory(assess_id=assessId, surgical_history=surgical_history, hospitalization=hospitalization, current_illness=current_illness, prev_accident_history=prev_accident_history, date=date)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesspastmedicalhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_medicalhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessPastMedicalHistory.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesspastmedicalhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def add_familyhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    description = request.POST.get('description')

    try:
        row = AssessFamilyHistory(assess_id=assessId, description=description)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessfamilyhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_familyhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessFamilyHistory.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessfamilyhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def add_medication(request):
    result = "success"

    assessId = request.POST['assessId']
    description = request.POST.get('description')
    postmva = request.POST.get('postmva')

    try:
        row = AssessMedication(medication=description, post_mva=postmva, assess_id=assessId)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessmedication
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_medication(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessMedication.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessmedication
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def add_allergy(request):
    result = "success"

    assessId = request.POST['assessId']
    description = request.POST.get('description')

    try:
        row = AssessAllergies(allergy=description, assess_id=assessId)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessallergies
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_allergy(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessAllergies.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessallergies
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def add_socialhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    marital_status = request.POST.get('marital_status')
    living_accommodations = request.POST.get('living_accommodations')
    elevator = request.POST.get('elevator')
    dependent = request.POST.get('dependent')
    age = request.POST.get('age')
    lives_withclaimant = request.POST.get('lives_withclaimant')

    try:
        row = AssessSocialHistory(marital_status=marital_status, living_accommodations=living_accommodations, elevator=elevator, dependent=dependent, age=age, lives_withclaimant=lives_withclaimant, assess_id=assessId)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesssocialhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return JsonResponse({'result':result, 'data':data})

def delete_socialhistory(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessSocialHistory.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assesssocialhistory
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def save_activitytolerance(request):
    result = "success"

    assessId = request.POST['assessId']
    household = request.POST.get('household')
    caregiving = request.POST.get('caregiving')
    personal = request.POST.get('personal')
    otherinfo = request.POST.get('otherinfo')

    exist = AssessActivityTolerances.objects.filter(assess_id=assessId)
    if len(exist) > 0:
        exist[0].household = household
        exist[0].caregiving = caregiving
        exist[0].personal = personal
        exist[0].otherinfo = otherinfo
        exist[0].save()
    else:
        try:
            row = AssessActivityTolerances(household=household, caregiving=caregiving, personal=personal, assess_id=assessId, otherinfo=otherinfo)
            row.save()
        except:
            result = "error"
    return JsonResponse({'result':result})

def add_occu(request):
    result = "success"

    assessId = request.POST['assessId']
    employment_status = request.POST.get('employment_status')
    company_name = request.POST.get('company_name')
    job_title = request.POST.get('job_title')
    years_employed = request.POST.get('years_employed')
    regular_hrs_weekly = request.POST.get('regular_hrs_weekly')
    job_duties = request.POST.get('job_duties')
    time_missed = request.POST.get('time_missed')
    option_cycle = request.POST.get('option_cycle')
    date_returned = request.POST.get('date_returned')
    modified_hrs_weekly = request.POST.get('modified_hrs_weekly')

    try:
        row = AssessOccupantionalStatus(employment_status=employment_status, company_name=company_name, job_title=job_title, years_employed=years_employed, regular_hrs_weekly=regular_hrs_weekly, job_duties=job_duties, time_missed=time_missed, option_cycle=option_cycle, date_returned=date_returned, modified_hrs_weekly=modified_hrs_weekly, assess_id=assessId)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessoccupantionalstatus
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return JsonResponse({'result':result, 'data':data})

def delete_occu(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessOccupantionalStatus.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessoccupantionalstatus
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def save_psychological(request):
    result = "success"

    assessId = request.POST['assessId']
    sleep = request.POST.get('sleep')
    num_awakingup_nightly = request.POST.get('num_awakingup_nightly')
    reason_awakened = request.POST.get('reason_awakened')
    description_mood = request.POST.get('description_mood')

    exist = AssessPsychologicalStatus.objects.filter(assess_id=assessId)
    if len(exist) > 0:
        exist[0].sleep = sleep
        exist[0].num_awakingup_nightly = num_awakingup_nightly
        exist[0].reason_awakened = reason_awakened
        exist[0].description_mood = description_mood
        exist[0].save()
    else:
        try:
            row = AssessPsychologicalStatus(sleep=sleep, num_awakingup_nightly=num_awakingup_nightly, reason_awakened=reason_awakened, description_mood=description_mood, assess_id=assessId)
            row.save()
        except:
            result = "error"
    return JsonResponse({'result':result})

def save_presentcomplaints(request):
    result = "success"

    assessId = request.POST['assessId']

    headache_location = request.POST.get('headache_location')
    headache_quality = request.POST.get('headache_quality')
    headache_frequency = request.POST.get('headache_frequency')
    headache_intensity = request.POST.get('headache_intensity')
    headache_migrains = request.POST.get('headache_migrains')
    headache_agrravating_factors = request.POST.get('headache_agrravating_factors')
    headache_relieving_factors = request.POST.get('headache_relieving_factors')
    headache_associated_symptoms = request.POST.get('headache_associated_symptoms')
    headache_notes = request.POST.get('headache_notes')

    shoulder_history = request.POST.get('shoulder_history')
    shoulder_frequency = request.POST.get('shoulder_frequency')
    shoulder_intensity = request.POST.get('shoulder_intensity')
    shoulder_location = request.POST.get('shoulder_location')
    shoulder_quality = request.POST.get('shoulder_quality')
    shoulder_agrravating_factors = request.POST.get('shoulder_agrravating_factors')
    shoulder_relieving_factors = request.POST.get('shoulder_relieving_factors')
    shoulder_associated_symptoms = request.POST.get('shoulder_associated_symptoms')
    shoulder_notes = request.POST.get('shoulder_notes')

    cervical_spine_history = request.POST.get('cervical_spine_history')
    cervical_spine_frequency = request.POST.get('cervical_spine_frequency')
    cervical_spine_intensity = request.POST.get('cervical_spine_intensity')
    cervical_spine_location = request.POST.get('cervical_spine_location')
    cervical_spine_quality = request.POST.get('cervical_spine_quality')
    cervical_spine_agrravating_factors = request.POST.get('cervical_spine_agrravating_factors')
    cervical_spine_relieving_factors = request.POST.get('cervical_spine_relieving_factors')
    cervical_spine_associated_symptoms = request.POST.get('cervical_spine_associated_symptoms')
    cervical_spine_notes = request.POST.get('cervical_spine_notes')

    lumber_spine_history = request.POST.get('lumber_spine_history')
    lumber_spine_frequency = request.POST.get('lumber_spine_frequency')
    lumber_spine_intensity = request.POST.get('lumber_spine_intensity')
    lumber_spine_location = request.POST.get('lumber_spine_location')
    lumber_spine_quality = request.POST.get('lumber_spine_quality')
    lumber_spine_agrravating_factors = request.POST.get('lumber_spine_agrravating_factors')
    lumber_spine_relieving_factors = request.POST.get('lumber_spine_relieving_factors')
    lumber_spine_associated_symptoms = request.POST.get('lumber_spine_associated_symptoms')
    lumber_spine_notes = request.POST.get('lumber_spine_notes')

    knee_history = request.POST.get('knee_history')
    knee_frequency = request.POST.get('knee_frequency')
    knee_intensity = request.POST.get('knee_intensity')
    knee_location = request.POST.get('knee_location')
    knee_quality = request.POST.get('knee_quality')
    knee_agrravating_factors = request.POST.get('knee_agrravating_factors')
    knee_relieving_factors = request.POST.get('knee_relieving_factors')
    knee_associated_symptoms = request.POST.get('knee_associated_symptoms')
    knee_notes = request.POST.get('knee_notes')

    ankle_foot_history = request.POST.get('ankle_foot_history')
    ankle_foot_frequency = request.POST.get('ankle_foot_frequency')
    ankle_foot_intensity = request.POST.get('ankle_foot_intensity')
    ankle_foot_location = request.POST.get('ankle_foot_location')
    ankle_foot_quality = request.POST.get('ankle_foot_quality')
    ankle_foot_agrravating_factors = request.POST.get('ankle_foot_agrravating_factors')
    ankle_foot_relieving_factors = request.POST.get('ankle_foot_relieving_factors')
    ankle_foot_associated_symptoms = request.POST.get('ankle_foot_associated_symptoms')
    ankle_foot_notes = request.POST.get('ankle_foot_notes')

    hand_wrist_history = request.POST.get('hand_wrist_history')
    hand_wrist_frequency = request.POST.get('hand_wrist_frequency')
    hand_wrist_intensity = request.POST.get('hand_wrist_intensity')
    hand_wrist_location = request.POST.get('hand_wrist_location')
    hand_wrist_quality = request.POST.get('hand_wrist_quality')
    hand_wrist_agrravating_factors = request.POST.get('hand_wrist_agrravating_factors')
    hand_wrist_relieving_factors = request.POST.get('hand_wrist_relieving_factors')
    hand_wrist_associated_symptoms = request.POST.get('hand_wrist_associated_symptoms')
    hand_wrist_notes = request.POST.get('hand_wrist_notes')

    otherinfo = request.POST.get('otherinfo')

    exist = AssessPresentComplaints.objects.filter(assess_id=assessId)
    if len(exist) > 0:
        exist[0].headache_location = headache_location
        exist[0].headache_quality = headache_quality
        exist[0].headache_frequency = headache_frequency
        exist[0].headache_intensity = headache_intensity
        exist[0].headache_migrains = headache_migrains
        exist[0].headache_agrravating_factors = headache_agrravating_factors
        exist[0].headache_relieving_factors = headache_relieving_factors
        exist[0].headache_associated_symptoms = headache_associated_symptoms
        exist[0].headache_notes = headache_notes

        exist[0].shoulder_history = shoulder_history
        exist[0].shoulder_frequency = shoulder_frequency
        exist[0].shoulder_intensity = shoulder_intensity
        exist[0].shoulder_location = shoulder_location
        exist[0].shoulder_quality = shoulder_quality
        exist[0].shoulder_agrravating_factors = shoulder_agrravating_factors
        exist[0].shoulder_relieving_factors = shoulder_relieving_factors
        exist[0].shoulder_associated_symptoms = shoulder_associated_symptoms
        exist[0].shoulder_notes = shoulder_notes

        exist[0].cervical_spine_history = cervical_spine_history
        exist[0].cervical_spine_frequency = cervical_spine_frequency
        exist[0].cervical_spine_intensity = cervical_spine_intensity
        exist[0].cervical_spine_location = cervical_spine_location
        exist[0].cervical_spine_quality = cervical_spine_quality
        exist[0].cervical_spine_agrravating_factors = cervical_spine_agrravating_factors
        exist[0].cervical_spine_relieving_factors = cervical_spine_relieving_factors
        exist[0].cervical_spine_associated_symptoms = cervical_spine_associated_symptoms
        exist[0].cervical_spine_notes = cervical_spine_notes

        exist[0].lumber_spine_history = lumber_spine_history
        exist[0].lumber_spine_frequency = lumber_spine_frequency
        exist[0].lumber_spine_intensity = lumber_spine_intensity
        exist[0].lumber_spine_location = lumber_spine_location
        exist[0].lumber_spine_quality = lumber_spine_quality
        exist[0].lumber_spine_agrravating_factors = lumber_spine_agrravating_factors
        exist[0].lumber_spine_relieving_factors = lumber_spine_relieving_factors
        exist[0].lumber_spine_associated_symptoms = lumber_spine_associated_symptoms
        exist[0].lumber_spine_notes = lumber_spine_notes

        exist[0].knee_history = knee_history
        exist[0].knee_frequency = knee_frequency
        exist[0].knee_intensity = knee_intensity
        exist[0].knee_location = knee_location
        exist[0].knee_quality = knee_quality
        exist[0].knee_agrravating_factors = knee_agrravating_factors
        exist[0].knee_relieving_factors = knee_relieving_factors
        exist[0].knee_associated_symptoms = knee_associated_symptoms
        exist[0].knee_notes = knee_notes

        exist[0].ankle_foot_history = ankle_foot_history
        exist[0].ankle_foot_frequency = ankle_foot_frequency
        exist[0].ankle_foot_intensity = ankle_foot_intensity
        exist[0].ankle_foot_location = ankle_foot_location
        exist[0].ankle_foot_quality = ankle_foot_quality
        exist[0].ankle_foot_agrravating_factors = ankle_foot_agrravating_factors
        exist[0].ankle_foot_relieving_factors = ankle_foot_relieving_factors
        exist[0].ankle_foot_associated_symptoms = ankle_foot_associated_symptoms
        exist[0].ankle_foot_notes = ankle_foot_notes

        exist[0].hand_wrist_history = hand_wrist_history
        exist[0].hand_wrist_frequency = hand_wrist_frequency
        exist[0].hand_wrist_intensity = hand_wrist_intensity
        exist[0].hand_wrist_location = hand_wrist_location
        exist[0].hand_wrist_quality = hand_wrist_quality
        exist[0].hand_wrist_agrravating_factors = hand_wrist_agrravating_factors
        exist[0].hand_wrist_relieving_factors = hand_wrist_relieving_factors
        exist[0].hand_wrist_associated_symptoms = hand_wrist_associated_symptoms
        exist[0].hand_wrist_notes = hand_wrist_notes

        exist[0].save()
    else:
        try:
            row = AssessPresentComplaints(headache_location=headache_location, headache_quality=headache_quality, headache_frequency=headache_frequency, headache_intensity=headache_intensity, headache_migrains=headache_migrains, headache_agrravating_factors=headache_agrravating_factors, headache_relieving_factors=headache_relieving_factors, headache_associated_symptoms=headache_associated_symptoms, headache_notes=headache_notes, cervical_spine_history=cervical_spine_history, cervical_spine_frequency=cervical_spine_frequency, cervical_spine_intensity=cervical_spine_intensity, cervical_spine_location=cervical_spine_location, cervical_spine_quality=cervical_spine_quality, cervical_spine_agrravating_factors=cervical_spine_agrravating_factors, cervical_spine_relieving_factors=cervical_spine_relieving_factors, cervical_spine_associated_symptoms=cervical_spine_associated_symptoms, cervical_spine_notes=cervical_spine_notes, lumber_spine_history=lumber_spine_history, lumber_spine_frequency=lumber_spine_frequency, lumber_spine_intensity=lumber_spine_intensity, lumber_spine_location=lumber_spine_location, lumber_spine_quality=lumber_spine_quality, lumber_spine_agrravating_factors=lumber_spine_agrravating_factors, lumber_spine_relieving_factors=lumber_spine_relieving_factors, lumber_spine_associated_symptoms=lumber_spine_associated_symptoms, lumber_spine_notes=lumber_spine_notes, knee_history=knee_history, knee_frequency=knee_frequency, knee_intensity=knee_intensity, knee_location=knee_location, knee_quality=knee_quality, knee_agrravating_factors=knee_agrravating_factors, knee_relieving_factors=knee_relieving_factors, knee_associated_symptoms=knee_associated_symptoms, knee_notes=knee_notes, ankle_foot_history=ankle_foot_history, ankle_foot_frequency=ankle_foot_frequency, ankle_foot_intensity=ankle_foot_intensity, ankle_foot_location=ankle_foot_location, ankle_foot_quality=ankle_foot_quality, ankle_foot_agrravating_factors=ankle_foot_agrravating_factors, ankle_foot_relieving_factors=ankle_foot_relieving_factors, ankle_foot_associated_symptoms=ankle_foot_associated_symptoms, ankle_foot_notes=ankle_foot_notes, hand_wrist_history=hand_wrist_history, hand_wrist_frequency=hand_wrist_frequency, hand_wrist_intensity=hand_wrist_intensity, hand_wrist_location=hand_wrist_location, hand_wrist_quality=hand_wrist_quality, hand_wrist_agrravating_factors=hand_wrist_agrravating_factors, hand_wrist_relieving_factors=hand_wrist_relieving_factors, hand_wrist_associated_symptoms=hand_wrist_associated_symptoms, hand_wrist_notes=hand_wrist_notes, shoulder_history=shoulder_history, shoulder_frequency=shoulder_frequency, shoulder_intensity=shoulder_intensity, shoulder_location=shoulder_location, shoulder_quality=shoulder_quality, shoulder_agrravating_factors=shoulder_agrravating_factors, shoulder_relieving_factors=shoulder_relieving_factors, shoulder_associated_symptoms=shoulder_associated_symptoms, shoulder_notes=shoulder_notes, assess_id=assessId, otherinfo=otherinfo)
            row.save()
        except:
            result = "error"
    return JsonResponse({'result':result})

def add_diagnose(request):
    result = "success"

    assessId = request.POST['assessId']
    description = request.POST.get('description')

    try:
        row = AssessDiagnoses(description=description, assess_id=assessId)
        row.save()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessdiagnoses
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def delete_diagnose(request):
    result = "success"

    assessId = request.POST['assessId']
    id = request.POST.get('id')

    try:
        row = AssessDiagnoses.objects.filter(assess_id=assessId, id=id)
        row.delete()
    except:
        result = "error"

    query = """
            SELECT *
            FROM tbl_assessdiagnoses
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()

    return JsonResponse({'result':result, 'data':data})

def save_referralquestions(request):
    result = "success"

    assessId = request.POST['assessId']
    income_replacement = request.POST.get('income_replacement')
    caregiver = request.POST.get('caregiver')
    non_earner = request.POST.get('non_earner')
    medical_rehabilitation_benefits = request.POST.get('medical_rehabilitation_benefits')
    minor_injury_guideline = request.POST.get('minor_injury_guideline')
    standard_questions = request.POST.get('standard_questions')
    otherinfo = request.POST.get('otherinfo')

    exist = AssessReferralQuestions.objects.filter(assess_id=assessId)
    if len(exist) > 0:
        exist[0].income_replacement = income_replacement
        exist[0].caregiver = caregiver
        exist[0].non_earner = non_earner
        exist[0].medical_rehabilitation_benefits = medical_rehabilitation_benefits
        exist[0].minor_injury_guideline = minor_injury_guideline
        exist[0].standard_questions = standard_questions
        exist[0].otherinfo = otherinfo
        exist[0].save()
    else:
        try:
            row = AssessReferralQuestions(income_replacement=income_replacement, caregiver=caregiver, non_earner=non_earner, medical_rehabilitation_benefits=medical_rehabilitation_benefits, minor_injury_guideline=minor_injury_guideline, standard_questions=standard_questions, assess_id=assessId, otherinfo=otherinfo)
            row.save()
        except:
            result = "error"
    return JsonResponse({'result':result})

def add_physicalexam(request):
    result = "success"

    assessId = request.POST['assessId']
    anklefoot = request.POST.get('anklefoot')
    cervical = request.POST.get('cervical')
    handwrist = request.POST.get('handwrist')
    knee = request.POST.get('knee')
    lumbarspine = request.POST.get('lumbarspine')
    neurologic = request.POST.get('neurologic')
    physicalintro = request.POST.get('physicalintro')
    shoulder = request.POST.get('shoulder')
    physicalexam = request.POST.get('physicalexam')

    exist = AssessPhysicalExam.objects.filter(assess_id=assessId)
    if len(exist) <= 0:
        try:
            row = AssessPhysicalExam(assess_id=assessId, anklefoot=anklefoot, cervical=cervical, handwrist=handwrist, knee=knee, lumbarspine=lumbarspine, neurologic=neurologic, physicalintro=physicalintro, shoulder=shoulder, physicalexam=physicalexam)
            row.save()
        except:
            result = "error"
    else:
        exist[0].anklefoot = anklefoot
        exist[0].cervical = cervical
        exist[0].handwrist = handwrist
        exist[0].knee = knee
        exist[0].lumbarspine = lumbarspine
        exist[0].neurologic = neurologic
        exist[0].physicalintro = physicalintro
        exist[0].shoulder = shoulder
        exist[0].physicalexam = physicalexam
        exist[0].save()

    query = """
            SELECT *
            FROM tbl_assessphysicalexam
            WHERE assess_id = '""" + str(assessId) + """'
            """
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    return JsonResponse({'result':result, 'data':data})



def assess_type(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            return render(request, 'assess_type.html', {'AssessType':AssessType.objects.all()})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def add_assesstype(request):
    result = ""
    try:
        add_assesstype = request.POST.get('add_assesstype')
        add_description = request.POST.get('add_description')

        existUser = AssessType.objects.filter(assess_type=add_assesstype)
        if len(existUser) > 0:
            result = "exist"
        else:
            row = AssessType(assess_type=add_assesstype, description=add_description)
            row.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def edit_assesstype(request):
    result = ""
    try:
        edit_id = request.POST.get('edit_id')
        edit_assesstype = request.POST.get('edit_assesstype')
        edit_description = request.POST.get('edit_description')

        existUser = AssessType.objects.filter(assess_type=edit_assesstype).exclude(id=edit_id)
        if len(existUser) > 0:
            result = "exist"
        else:
            row = AssessType.objects.filter(id=edit_id)[0]
            row.assess_type = edit_assesstype
            row.description = edit_description
            row.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def delete_assesstype(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            AssessType.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})



def assess_location(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            return render(request, 'assess_location.html', {'AssessLocation':AssessLocation.objects.all()})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def add_location(request):
    result = ""
    try:
        add_name = request.POST.get('add_name')
        add_location = request.POST.get('add_location')

        existUser = AssessLocation.objects.filter(clinic=add_name)
        if len(existUser) > 0:
            result = "exist"
        else:
            location = AssessLocation(clinic=add_name, location=add_location)
            location.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def edit_location(request):
    result = ""
    try:
        edit_id = request.POST.get('edit_id')
        edit_name = request.POST.get('edit_name')
        edit_location = request.POST.get('edit_location')

        existUser = AssessLocation.objects.filter(clinic=edit_name).exclude(id=edit_id)
        if len(existUser) > 0:
            result = "exist"
        else:
            location = AssessLocation.objects.filter(id=edit_id)[0]
            location.clinic = edit_name
            location.location = edit_location
            location.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def delete_location(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            AssessLocation.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})



def question_banklist(request):
    if request.session.has_key('username'):
        query = "SELECT a.id, a.agency, b.name, a.question_type, a.question FROM tbl_questionbanklist AS a LEFT JOIN tbl_referralagency AS b ON a.agency = b.id"
        with connection.cursor() as cursor:
            cursor.execute(query)
            questions = cursor.fetchall()
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            return render(request, 'question_banklist.html', {'ReferralAgency':ReferralAgency.objects.all(), "Questions": questions})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def add_question(request):
    result = ""
    try:
        add_agency = request.POST.get('add_agency')
        add_questiontype = request.POST.get('add_questiontype')
        add_question = request.POST.get('add_question')

        existUser = QuestionBankList.objects.filter(question=add_question)
        if len(existUser) > 0:
            result = "exist"
        else:
            agency = QuestionBankList(agency=add_agency, question=add_question, question_type=add_questiontype)
            agency.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def edit_question(request):
    result = ""
    try:
        edit_id = request.POST.get('edit_id')
        edit_agency = request.POST.get('edit_agency')
        edit_questiontype = request.POST.get('edit_questiontype')
        edit_question = request.POST.get('edit_question')

        existQuestion = QuestionBankList.objects.filter(question=edit_question).exclude(id=edit_id)
        if len(existQuestion) > 0:
            result = "exist"
        else:
            question = QuestionBankList.objects.filter(id=edit_id)[0]
            question.agency = edit_agency
            question.questiontype = edit_questiontype
            question.question = edit_question
            question.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def delete_question(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            QuestionBankList.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})



def referral_agency(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            return render(request, 'referral_agency.html', {'ReferralAgency':ReferralAgency.objects.all()})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def add_referralagency(request):
    result = ""
    try:
        add_referralagency = request.POST.get('add_referralagency')
        add_description = request.POST.get('add_description')

        existUser = ReferralAgency.objects.filter(name=add_referralagency)
        if len(existUser) > 0:
            result = "exist"
        else:
            agency = ReferralAgency(name=add_referralagency, description=add_description)
            agency.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def edit_referralagency(request):
    result = ""
    try:
        edit_id = request.POST.get('edit_id')
        edit_referralagency = request.POST.get('edit_referralagency')
        edit_description = request.POST.get('edit_description')

        existAgency = ReferralAgency.objects.filter(name=edit_referralagency).exclude(id=edit_id)
        if len(existAgency) > 0:
            result = "exist"
        else:
            agency = ReferralAgency.objects.filter(id=edit_id)[0]
            agency.name = edit_referralagency
            agency.description = edit_description
            agency.save()
            result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def delete_referralagency(request):
    if request.method == "POST":
        try:
            id = int(request.POST.get('id'))
            ReferralAgency.objects.filter(id=id).delete()
        except:
            print("except")

    return JsonResponse({'result':'success'})


def scheduler(request):
    if request.session.has_key('username'):
        if request.session['userrole'] == "System Admin" or request.session['userrole'] == "Intake Agent" or request.session['userrole'] == "Doctor" or request.session['userrole'] == "Referral Source" :
            return render(request, 'scheduler_ime.html', {
                'doctors':User.objects.filter(role="Doctor"), 
                'agents':User.objects.filter(role="Intake Agent"),
                'locations':AssessLocation.objects.all()
            })        
        else:
            return render(request, 'login.html')
        
    else:
        return render(request, 'login.html')

def saveScheduleSheet(request):
    result = ""
    try:
        week_day = request.POST.get('week_day')
        coord = request.POST.get('coord')
        status = request.POST.get('status')
        userId = request.POST.get('userId')

        exist = Scheduler.objects.filter(dateArr=week_day, userId=userId)
        if len(exist) > 0:
            query = "UPDATE tbl_scheduler SET indexArr = '" + str(coord) + "' WHERE dateArr = '" + str(week_day) + "' AND userId = '" + str(userId) + "'"
            connection.cursor().execute(query)
        else:
            row = Scheduler(dateArr=week_day, indexArr=coord, userId=userId, status=status)
            row.save()
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def getScheduleSheet(request):
    result = ""
    try:
        week_day = request.POST.get('week_day')
        userId = request.POST.get('userId')

        exist = Scheduler.objects.filter(dateArr=week_day, userId=userId)[0].indexArr
        result = "success"
        return JsonResponse({'result':result, 'indexArr': exist})
    except:
        result = "error"
        return JsonResponse({'result':result, 'indexArr': "none"})

def requestSchedule(request):
    # Save to Mailbox
    if request.session.get("userrole") == "System Admin":
        admins = User.objects.filter(role='Doctor')
    elif request.session.get("userrole") == "Referral Source":
        admins = User.objects.filter(role='Doctor')
    dt = datetime.datetime.now()
    dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    subject = "Doctor's Availability Request"
    content = 'Please update the Date & Time Sheet for a few months.'
    message = 'Please update the Date & Time Sheet for a few months.'
    
    admin_emails = []
    for admin in admins:
        mailItem = MailBox(fromUser=request.session.get("userid"), toUser=admin.id, mailType="RequestSchedule", orderId='', header=subject, content=content, dateTime=dateTime)
        mailItem.save()

        admin_emails.append(str(admin.email))

    # Send Order Email to Admins.
    if admin_emails:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = admin_emails
        send_mail( subject, message, email_from, recipient_list )
    return JsonResponse({'result':'success'})

def sendSchedule(request):
    # Save to Mailbox
    if request.session.get("userrole") == "System Admin":
        admins = User.objects.filter(role='Referral Source')
    elif request.session.get("userrole") == "Doctor":
        admins = User.objects.filter(role='System Admin')
    dt = datetime.datetime.now()
    dateTime = dt.strftime("%Y-%m-%d %H:%M:%S")
    subject = "Doctor's Availability is updated."
    content = 'Please check the Date & Time Sheet to fill clients in'
    message = 'Please check the Date & Time Sheet to fill clients in.'
    
    admin_emails = []
    for admin in admins:
        mailItem = MailBox(fromUser=request.session.get("userid"), toUser=admin.id, mailType="SendScheduleSheet", orderId='', header=subject, content=content, dateTime=dateTime)
        mailItem.save()

        admin_emails.append(str(admin.email))

    # Send Order Email to Admins.
    # if admin_emails:
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = admin_emails
    #     send_mail( subject, message, email_from, recipient_list )
    return JsonResponse({'result':'success'})

def saveScheduled(request):
    result = ""
    try:
        weekId = request.POST.get('weekId')
        indexArr = request.POST.get('indexArr')
        intakeAgent = request.POST.get('intakeAgent')
        doctorId = request.POST.get('doctorId')
        locationId = request.POST.get('locationId')
        rowId = request.POST.get('rowId')
        scheduledTime = request.POST.get('scheduledTime')

        if rowId != "none":
            query = "UPDATE tbl_scheduledtime SET intakeAgent = '" + str(intakeAgent) + "', locationId = '" + str(locationId) + "' WHERE id = '" + str(rowId) + "'"
            connection.cursor().execute(query)
        else:
            row = ScheduledTime(weekId=weekId, indexArr=indexArr, intakeAgent=intakeAgent, doctorId=doctorId, locationId=locationId, adminId=request.session.get("userid"), scheduledTime=scheduledTime, alertStatus="0")
            row.save()
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result})

def getScheduled(request):
    result = ""
    try:
        weekId = request.POST.get('weekId')
        doctorId = request.POST.get('doctorId')
        query = "SELECT id, indexArr, intakeAgent, locationId, adminId FROM tbl_scheduledtime WHERE weekId = '" + weekId + "' AND doctorId = " + doctorId
        with connection.cursor() as cursor:
            cursor.execute(query)
            exist = cursor.fetchall()
        
        result = "success"
    except:
        result = "error"

    return JsonResponse({'result':result, 'data':exist})