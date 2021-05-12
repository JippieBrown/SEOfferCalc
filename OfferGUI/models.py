from OfferGUI import db, login_manager
from OfferGUI import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class static_costs_commissioning_tools(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())

class static_costs_installation_tools(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())

class static_costs_site_equipment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())

class static_costs_staff(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())
    price_reg_inquiry_RC = db.Column(db.String())
    price_reg_inquiry_OE = db.Column(db.String())
    price_reg_inquiry_RC_DE = db.Column(db.String())

class static_costs_testing_tools(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())

class static_costs_travel_accommodation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    service = db.Column(db.String())

class temp_inquiry(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    department = db.Column(db.String())
    project_name = db.Column(db.String())
    country = db.Column(db.String())
    city = db.Column(db.String())
    inquiry_date = db.Column(db.String())
    plant_type = db.Column(db.String())    
    validity = db.Column(db.String())
    protection_class_indoor = db.Column(db.String())
    protection_class_outdoor = db.Column(db.String())
    calc_for = db.Column(db.String())
    busbar = db.Column(db.String())
    number_of_bays = db.Column(db.String())
    supervision = db.Column(db.String())
    commissioning = db.Column(db.String())
    mpd = db.Column(db.String())
    language = db.Column(db.String())
    tools = db.Column(db.String())
    hv_test = db.Column(db.String())
    transport = db.Column(db.String())
    sec_works = db.Column(db.String())
    sec_works_no_of_bays = db.Column(db.String())
    earthing = db.Column(db.String())
    pd_measurement = db.Column(db.String())
    psd = db.Column(db.String())
    actas = db.Column(db.String())
    libo = db.Column(db.String())
    customer_training = db.Column(db.String())
    indoor_crane = db.Column(db.String())
    dc_supply = db.Column(db.String())
    hv_plugs = db.Column(db.String())
    hv_plug_size = db.Column(db.String())
    remark = db.Column(db.String())
    offer_until = db.Column(db.String())
    kick_off_meeting = db.Column(db.String())

class temp_project_info(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String())
    project_manager_dept = db.Column(db.String())
    order_indicator = db.Column(db.String())
    site = db.Column(db.String())
    customer = db.Column(db.String())
    ## further info
    calc_for = db.Column(db.String())
    date = db.Column(db.String())
    cost_determination = db.Column(db.String())
    editor = db.Column(db.String())
    project_id = db.Column(db.String())
    ## plant info
    plant_type = db.Column(db.String())
    busbar = db.Column(db.String())
    number_of_bays = db.Column(db.Integer())
    commissioning = db.Column(db.String())
    
class temp_staff_costs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Service = db.Column(db.String(length=30), nullable=False, unique=True)
    UnitPrice = db.Column(db.Integer(), nullable=False)
    RentalMode = db.Column(db.String(), nullable=False)
    RentalUnits = db.Column(db.String(), nullable=False)
    Remark = db.Column(db.String(length=60), nullable=False)
    Sum = db.Column(db.Integer(), nullable=False)
    # def __repr__(self):
    #     return f'staff_costs {self.name}'
    
class temp_tool_costs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Service = db.Column(db.String(length=30), nullable=False, unique=True)
    UnitPrice = db.Column(db.Integer(), nullable=False)
    RentalMode = db.Column(db.String(), nullable=False)
    RentalPeriod = db.Column(db.String(), nullable=False)
    Remark = db.Column(db.String(length=60), nullable=False)
    Sum = db.Column(db.Integer(), nullable=False)
    # def __repr__(self):
    #     return f'staff_costs {self.name}'

class dropdown_elements(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    plant_type = db.Column(db.String())
    busbar = db.Column(db.String())
    calc_for = db.Column(db.String())
    yes_no = db.Column(db.String())
    languages = db.Column(db.String())
    #check database
    rental_mode = db.Column(db.String())
    # def __repr__(self):
    #     return f'dropdown_elements {self.name}'

class collected_projects(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(), unique=True)
    project_manager_dept = db.Column(db.String())
    order_indicator = db.Column(db.String())
    site = db.Column(db.String())
    customer = db.Column(db.String())
    ## further info
    calc_for = db.Column(db.String())
    date = db.Column(db.String())
    cost_determination = db.Column(db.String())
    editor = db.Column(db.String())
    project_id = db.Column(db.String())
    ## plant info
    plant_type = db.Column(db.String())
    busbar = db.Column(db.String())
    number_of_bays = db.Column(db.Integer())
    commissioning = db.Column(db.String())
    # gascomp_empty = StringField(label='Gas compartments (empty)')
    # gascomp_pref = StringField(label='Gas compartments (prefilled)')
    # assembly_indoor = StringField(label='Assembly (indoor)')
    # assembly_outdoor = StringField(label='Assembly (outdoor)')
    # harting_plugs = StringField(label='Harting plugs')
    # ditec_seals = StringField(label='Ditec seals')
    # steel_supp_s = StringField(label='Steel support (small)')
    # steel_supp_m = StringField(label='Steel support (medium)')
    # steel_supp_l = StringField(label='Steel support (large)')
    # drives = StringField(label='Drives')
    # core_drilling = StringField(label='Core drillings')
    # converter = StringField(label='Converters')
    # outdoor_bushing= StringField(label='Outdoor bushings')
    # ## general info
    # workdays_per_week = IntegerField(label='Workdays per week')
    # hours_per_day = IntegerField(label='Hours per day')
    # number_of_site_manager = IntegerField(label='Number of site managers')
    # number_of_commissioning_engineers = IntegerField(label='Number of commissioning engineers')
    # transport_weeks_tools = IntegerField(label='Transport weeks for tools')
    # transport_weeks_HVTE = IntegerField(label='Transport weeks for HV-Test equipment')
    # arrival_departure_days = IntegerField(label='Arrival and departure days')
    # country_factor = IntegerField(label='Country factor')
    # customer_training_days = IntegerField(label='Customer training days')
    # # inquiry info
    # site_management = SelectField(u'Site management', coerce=str)
    # commissioning = SelectField(u'Commissioning', coerce=str)
    # manpower = SelectField(u'Manpower diagramm', coerce=str)
    # manpower_language = SelectField(u'Language', coerce=str)
    # tools = SelectField(u'Tools', coerce=str)
    # def __repr__(self):
    #     return f'project_info {self.name}'   