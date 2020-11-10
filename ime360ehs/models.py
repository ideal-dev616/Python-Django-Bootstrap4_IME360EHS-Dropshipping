from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, 
                    role, 
                    status, 
                    first_name, 
                    last_name, 
                    email, 
                    phone, 
                    extension, 
                    signature,
                    password=None,
                    is_superuser=False):
        user = User(email=email, 
                    role=role, 
                    status=status, 
                    first_name=first_name, 
                    last_name=last_name, 
                    phone=phone, 
                    extension=extension, 
                    signature=signature,
                    is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user
    

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=200)
    extension = models.CharField(max_length=200)
    signature = models.CharField(max_length=200)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    check = models.CharField(default="", max_length=200)
    branch = models.CharField(default="", max_length=200)
    institute = models.CharField(default="", max_length=200)
    account = models.CharField(default="", max_length=200)
    report_fee = models.CharField(default="", max_length=200)

    address = models.TextField(default="", max_length=200)
    cpso_id = models.CharField(default="", max_length=200)
    cmpa_id = models.CharField(default="", max_length=200)
    physician_type = models.CharField(default="", max_length=200)
    bio = models.CharField(default="", max_length=200)

    neurological = models.TextField(default="")
    shoulder = models.TextField(default="")
    cervical = models.TextField(default="")
    lumbarspine = models.TextField(default="")
    knee = models.TextField(default="")
    ankle = models.TextField(default="")
    hand = models.TextField(default="")

    USERNAME_FIELD ="email"

    objects = UserManager()
    
    class Meta():
        db_table = 'tbl_users'

    def get_id(self):
        return str(self.id)

class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=200)
    motto_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    ship_cost = models.IntegerField()
    note_profile = models.TextField()
    address_type = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    clinic_users = models.TextField()

    class Meta():
        db_table = 'tbl_clinics'

    def clinicusers_as_list(self):
        return str(self.clinic_users).split(',')

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    segment = models.CharField(max_length=200, default="")
    product_code = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    cost = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    markup = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    retail = models.CharField(max_length=200)
    product_image = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    service_cost = models.CharField(max_length=200)
    service_markup = models.CharField(max_length=200)
    service_retail = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_products'

class CustomOrderSheet(models.Model):
    id = models.AutoField(primary_key=True)
    clinic_id = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_customordersheet'

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    clinic_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    po_number = models.CharField(max_length=200)
    order_date = models.CharField(max_length=200)
    order_note = models.TextField(null=True, blank=True)
    
    class Meta():
        db_table = 'tbl_orders'

class OrderedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    qty = models.IntegerField(null=True, blank=True, default=0)
    
    class Meta():
        db_table = 'tbl_orderedproduct'

class OrderTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(default="", max_length=200)
    product_id = models.TextField()
    user_id = models.CharField(default="", max_length=200)

    class Meta():
        db_table = 'tbl_order_template'


class ReferralAgency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    class Meta():
        db_table = 'tbl_referralagency'

class QuestionBankList(models.Model):
    id = models.AutoField(primary_key=True)
    agency = models.CharField(max_length=200)
    question_type = models.CharField(null=True, blank=True, max_length=200)
    question = models.TextField()
    
    class Meta():
        db_table = 'tbl_questionbanklist'

class AssessLocation(models.Model):
    id = models.AutoField(primary_key=True)
    clinic = models.CharField(max_length=200)
    location = models.TextField()
    
    class Meta():
        db_table = 'tbl_assesslocation'

    def getClinic(self, id):
        return self.filter(id=id)[0].clinic

class AssessType(models.Model):
    id = models.AutoField(primary_key=True)
    assess_type = models.CharField(max_length=200)
    description = models.TextField()
    
    class Meta():
        db_table = 'tbl_assesstype'

class AssessManageName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    class Meta():
        db_table = 'tbl_assessmanagename'



class Assessment(models.Model):
    id = models.AutoField(primary_key=True)

    # general form
    referral_agency = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    assess_type = models.CharField(max_length=200)
    insurance_company = models.CharField(max_length=200)
    date_of_loss = models.CharField(max_length=200)
    claimant_mr = models.CharField(max_length=200)
    claimant_fname = models.CharField(max_length=200)
    claimant_lname = models.CharField(max_length=220)
    birthday = models.CharField(max_length=200)
    gender = models.CharField(max_length=220)
    claim_no = models.CharField(max_length=220)
    physician = models.CharField(max_length=200)
    intake_agent = models.CharField(max_length=220)
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=220)
    interpreter = models.CharField(max_length=220)

    class Meta():
        db_table = 'tbl_assessment'

class AssessDocSummary(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    physician = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    description = models.TextField()
    disputed = models.CharField(max_length=200)
    diagnostic_exam = models.CharField(max_length=200)

    class Meta():
        db_table = 'tbl_assessdocsummary'

class AssessMVADetails(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(max_length=200)
    id_type = models.CharField(max_length=200)
    pos_vehicle = models.CharField(max_length=200)
    num_occupants = models.CharField(max_length=200)
    accident_location = models.CharField(max_length=200)
    accident_description = models.TextField()
    seatbelt = models.CharField(max_length=200)
    airbags = models.CharField(max_length=200)
    head_injury = models.CharField(max_length=200)
    conscious_loss = models.CharField(max_length=200)
    bodily_impact = models.CharField(max_length=200)
    exit_vehicle = models.CharField(max_length=200)
    responding_units = models.CharField(max_length=200)
    towed = models.CharField(max_length=200)
    damage_detail_known = models.CharField(max_length=200)
    damage_to_vehicle = models.CharField(max_length=200)
    vehicle_make = models.CharField(max_length=200)
    vehicle_model = models.CharField(max_length=200)
    vehicle_year = models.CharField(max_length=200)
    hospital_visit = models.CharField(max_length=200)
    hospital_name = models.CharField(max_length=200)
    doctor_name = models.CharField(default="", max_length=200)
    num_days_after = models.CharField(max_length=200)
    see_family_doctor = models.CharField(max_length=200)
    xray_taken = models.CharField(max_length=200)
    first_facility_visited = models.CharField(max_length=200)
    other_info = models.TextField()

    class Meta():
        db_table = 'tbl_assessmvadetails'

class AssessTreatToDate(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    id_type = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    rehab_facility = models.CharField(max_length=200)
    address_country = models.CharField(max_length=200)
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=200)
    address_province = models.CharField(max_length=200)
    address_postal = models.CharField(max_length=200)
    frequency_visits = models.CharField(max_length=200)
    treat_duration = models.CharField(max_length=200)
    treat_type = models.CharField(max_length=200)
    date_fvisit = models.CharField(max_length=200)
    date_lvisit = models.CharField(max_length=200)
    attending_status = models.CharField(max_length=200)

    class Meta():
        db_table = 'tbl_assesstreattodate'

class AssessPastMedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    surgical_history = models.CharField(max_length=200)
    hospitalization = models.CharField(max_length=200)
    current_illness = models.CharField(max_length=200)
    prev_accident_history = models.CharField(max_length=200)
    date = models.CharField(max_length=200)

    class Meta():
        db_table = 'tbl_assesspastmedicalhistory'

class AssessFamilyHistory(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    description = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assessfamilyhistory'

class AssessMedication(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    medication = models.CharField(max_length=200)
    post_mva = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assessmedication'

class AssessAllergies(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    allergy = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assessallergies'

class AssessSocialHistory(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    marital_status = models.CharField(max_length=200)
    living_accommodations = models.CharField(max_length=200)
    elevator = models.CharField(max_length=200)
    dependent = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    lives_withclaimant = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assesssocialhistory'

class AssessActivityTolerances(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    household = models.CharField(max_length=200)
    caregiving = models.CharField(max_length=200)
    personal = models.CharField(max_length=200)
    otherinfo = models.TextField(default="")
    
    class Meta():
        db_table = 'tbl_assessactivitytolerances'

class AssessOccupantionalStatus(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    employment_status = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    years_employed = models.CharField(max_length=200)
    regular_hrs_weekly = models.CharField(max_length=200)
    job_duties = models.TextField()
    time_missed = models.CharField(max_length=200)
    option_cycle = models.CharField(max_length=200)
    date_returned = models.CharField(max_length=200)
    modified_hrs_weekly = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assessoccupantionalstatus'

class AssessPsychologicalStatus(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    sleep = models.CharField(max_length=200)
    num_awakingup_nightly = models.CharField(max_length=200)
    reason_awakened = models.CharField(max_length=200)
    description_mood = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assesspsychologicalstatus'

class AssessPresentComplaints(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)

    headache_location = models.CharField(max_length=200)
    headache_quality = models.CharField(max_length=200)
    headache_frequency = models.CharField(max_length=200)
    headache_intensity = models.CharField(max_length=200)
    headache_migrains = models.CharField(max_length=200)
    headache_agrravating_factors = models.CharField(max_length=200)
    headache_relieving_factors = models.CharField(max_length=200)
    headache_associated_symptoms = models.CharField(max_length=200)
    headache_notes = models.TextField()

    shoulder_history = models.CharField(max_length=200)
    shoulder_frequency = models.CharField(max_length=200)
    shoulder_intensity = models.CharField(max_length=200)
    shoulder_location = models.CharField(max_length=200)
    shoulder_quality = models.CharField(max_length=200)
    shoulder_agrravating_factors = models.CharField(max_length=200)
    shoulder_relieving_factors = models.CharField(max_length=200)
    shoulder_associated_symptoms = models.CharField(max_length=200)
    shoulder_notes = models.TextField()

    cervical_spine_history = models.CharField(max_length=200)
    cervical_spine_frequency = models.CharField(max_length=200)
    cervical_spine_intensity = models.CharField(max_length=200)
    cervical_spine_location = models.CharField(max_length=200)
    cervical_spine_quality = models.CharField(max_length=200)
    cervical_spine_agrravating_factors = models.CharField(max_length=200)
    cervical_spine_relieving_factors = models.CharField(max_length=200)
    cervical_spine_associated_symptoms = models.CharField(max_length=200)
    cervical_spine_notes = models.TextField()

    lumber_spine_history = models.CharField(max_length=200)
    lumber_spine_frequency = models.CharField(max_length=200)
    lumber_spine_intensity = models.CharField(max_length=200)
    lumber_spine_location = models.CharField(max_length=200)
    lumber_spine_quality = models.CharField(max_length=200)
    lumber_spine_agrravating_factors = models.CharField(max_length=200)
    lumber_spine_relieving_factors = models.CharField(max_length=200)
    lumber_spine_associated_symptoms = models.CharField(max_length=200)
    lumber_spine_notes = models.TextField()

    knee_history = models.CharField(max_length=200)
    knee_frequency = models.CharField(max_length=200)
    knee_intensity = models.CharField(max_length=200)
    knee_location = models.CharField(max_length=200)
    knee_quality = models.CharField(max_length=200)
    knee_agrravating_factors = models.CharField(max_length=200)
    knee_relieving_factors = models.CharField(max_length=200)
    knee_associated_symptoms = models.CharField(max_length=200)
    knee_notes = models.TextField()

    ankle_foot_history = models.CharField(max_length=200)
    ankle_foot_frequency = models.CharField(max_length=200)
    ankle_foot_intensity = models.CharField(max_length=200)
    ankle_foot_location = models.CharField(max_length=200)
    ankle_foot_quality = models.CharField(max_length=200)
    ankle_foot_agrravating_factors = models.CharField(max_length=200)
    ankle_foot_relieving_factors = models.CharField(max_length=200)
    ankle_foot_associated_symptoms = models.CharField(max_length=200)
    ankle_foot_notes = models.TextField()

    hand_wrist_history = models.CharField(max_length=200)
    hand_wrist_frequency = models.CharField(max_length=200)
    hand_wrist_intensity = models.CharField(max_length=200)
    hand_wrist_location = models.CharField(max_length=200)
    hand_wrist_quality = models.CharField(max_length=200)
    hand_wrist_agrravating_factors = models.CharField(max_length=200)
    hand_wrist_relieving_factors = models.CharField(max_length=200)
    hand_wrist_associated_symptoms = models.CharField(max_length=200)
    hand_wrist_notes = models.TextField()

    shoulder_history = models.CharField(max_length=200)
    shoulder_frequency = models.CharField(max_length=200)
    shoulder_intensity = models.CharField(max_length=200)
    shoulder_location = models.CharField(max_length=200)
    shoulder_quality = models.CharField(max_length=200)
    shoulder_agrravating_factors = models.CharField(max_length=200)
    shoulder_relieving_factors = models.CharField(max_length=200)
    shoulder_associated_symptoms = models.CharField(max_length=200)
    shoulder_notes = models.TextField()

    shoulder_history = models.CharField(max_length=200)
    shoulder_frequency = models.CharField(max_length=200)
    shoulder_intensity = models.CharField(max_length=200)
    shoulder_location = models.CharField(max_length=200)
    shoulder_quality = models.CharField(max_length=200)
    shoulder_agrravating_factors = models.CharField(max_length=200)
    shoulder_relieving_factors = models.CharField(max_length=200)
    shoulder_associated_symptoms = models.CharField(max_length=200)
    shoulder_notes = models.TextField()

    otherinfo = models.TextField(default="")
    
    class Meta():
        db_table = 'tbl_assesspresentcomplaints'

class AssessPhysicalExam(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    physicalintro = models.TextField(default="")
    neurologic = models.TextField(default="")
    shoulder = models.TextField(default="")
    cervical = models.TextField(default="")
    lumbarspine = models.TextField(default="")
    knee = models.TextField(default="")
    anklefoot = models.TextField(default="")
    handwrist = models.TextField(default="")
    physicalexam = models.TextField(default="")
    
    class Meta():
        db_table = 'tbl_assessphysicalexam'

class AssessDiagnoses(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    description = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_assessdiagnoses'

class AssessReferralQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    assess_id = models.CharField(default="", max_length=200)
    income_replacement = models.CharField(max_length=200)
    caregiver = models.CharField(max_length=200)
    non_earner = models.CharField(max_length=200)
    medical_rehabilitation_benefits = models.CharField(max_length=200)
    minor_injury_guideline = models.CharField(max_length=200)
    standard_questions = models.CharField(max_length=200)

    otherinfo = models.TextField(default="")
    
    class Meta():
        db_table = 'tbl_assessreferralquestions'



class ClinicUsers(models.Model):
    id = models.AutoField(primary_key=True)
    cmanager = models.CharField(max_length=200)
    cuser = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_clinicusers'

class MailBox(models.Model):
    id = models.AutoField(primary_key=True)
    fromUser = models.CharField(max_length=200)
    toUser = models.CharField(max_length=200)
    mailType = models.CharField(max_length=200)
    orderId = models.CharField(max_length=200)
    header = models.CharField(max_length=200)
    content = models.TextField()
    dateTime = models.CharField(max_length=200)
    
    class Meta():
        db_table = 'tbl_mailbox'

class BackOrder(models.Model):
    id = models.AutoField(primary_key=True)
    invoiceDate = models.CharField(max_length=200)
    invoiceId = models.CharField(max_length=200)
    orderId = models.CharField(max_length=200)
    productId = models.CharField(max_length=200)
    invoiced = models.CharField(max_length=200)
    payment = models.CharField(max_length=200)
    userId = models.CharField(max_length=200)
    packingslipURL = models.CharField(max_length=220)

    class Meta():
        db_table = 'tbl_backorder'

class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)

    dateArr = models.CharField(max_length=200)
    indexArr = models.TextField()
    userId = models.CharField(max_length=220)
    status = models.CharField(max_length=220)

    class Meta():
        db_table = 'tbl_scheduler'

class ScheduledTime(models.Model):
    id = models.AutoField(primary_key=True)

    weekId = models.CharField(max_length=200)
    indexArr = models.TextField()
    intakeAgent = models.CharField(max_length=200)
    doctorId = models.CharField(max_length=200)
    locationId = models.CharField(max_length=200)
    adminId = models.CharField(max_length=200)
    scheduledTime = models.DateTimeField(null=True, blank=True)
    alertStatus = models.CharField(max_length=200)

    class Meta():
        db_table = 'tbl_scheduledTime'