from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from OfferGUI.models import User, collected_projects

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists!')

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6, max=1000), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):

    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')

class HomeForm(FlaskForm):
    project = SelectField(label='Project', coerce=str)

class ProjectForm(FlaskForm):
    '''
    #choices (represented by coerce) of selectfields in routes.py --> project_page

    '''    
    # def validate_project_name(self, project_name_to_check):
    #     project_name = projinquiry_xmlect_info.query.filter_by(project_name=project_name_to_check.data).first()
    #     if project_name:
    #         raise ValidationError('Project name already exists!')

    def validate_project_id(self, project_id_to_check):
        project_id = collected_projects.query.filter_by(project_id=project_id_to_check.data).first()
        if project_id:
            raise ValidationError('Project ID already exists!')
    ### Submit (Save-Button)
    submit = SubmitField(label='Save')
    # inquiry info
    first_name                 = StringField(label="Firstname")         
    last_name                  = StringField(label="Lastname")         
    department                 = StringField(label="Department")         
    project_name               = StringField(label='Project name')             
    country                    = StringField(label="Country")     
    city                       = StringField(label="City")     
    inquiry_date               = DateField(label="Inquiry date", format='%Y-%m-%d')             
    plant_type                 = SelectField(u'Plant type', coerce=str)         
    validity                   = SelectField(u'Validity', coerce=str)
    protection_class_indoor    = SelectField(u'Protection class indoor', coerce=str)                      
    protection_class_outdoor   = SelectField(u'Protection class outdoor', coerce=str)                          
    calc_for                   = SelectField(u'Calculation for', coerce=str, validators=[DataRequired()])         
    busbar                     = SelectField(u'Busbar', coerce=str)     
    number_of_bays             = IntegerField(label='Number of bays')             
    supervision                = SelectField(u'Site management', coerce=str)         
    commissioning              = SelectField(u'Commissioning', coerce=str)            
    mpd                        = SelectField(u'Manpower diagramm', coerce=str) 
    language                   = SelectField(u'Language', coerce=str)         
    tools                      = SelectField(u'Tools', coerce=str)     
    hv_test_equipment          = SelectField(u'HV-Test equipment', coerce=str)     
    transport                  = SelectField(u'Transports', coerce=str)
    sec_works                  = SelectField(u'Secondary works', coerce=str)         
    sec_works_no_of_bays       = IntegerField(label='Number of bays')                      
    earthing                   = SelectField(u'Earthing', coerce=str)         
    pd_measurement             = SelectField(u'HV-Test / PD-measurement', coerce=str)             
    psd                        = SelectField(u'PSD Commissioning', coerce=str) 
    actas                      = SelectField(u'ACTAS', coerce=str)     
    libo                       = SelectField(u'Arc guard systems', coerce=str)
    customer_training          = SelectField(u'Customer training', coerce=str)                
    indoor_crane               = SelectField(u'Indoor crane', coerce=str)             
    dc_supply                  = SelectField(u'DC supply', coerce=str) 
    hv_plugs                   = SelectField(u'HV plugs', coerce=str)         
    hv_plug_size               = SelectField(u'HV plug size', coerce=str)            
    remark                     = TextAreaField(label="Remark")     
    offer_until                = DateField(label="Offer until", format='%Y-%m-%d')          
    kick_off_meeting           = DateField(label="Kick off meeting", format='%Y-%m-%d')                 

    ## project info
    project_id = StringField(label='Project ID', validators=[DataRequired()])
    order_indicator = StringField(label='Oder indicator')
    customer = StringField(label='Customer', validators=[DataRequired()])
    date_of_editing = DateField(label='Date of editing', format='%Y-%m-%d')
    editor = SelectField(u'Editor', coerce=str)
    



    gascomp_empty = StringField(label='Gas compartments (empty)')
    gascomp_pref = StringField(label='Gas compartments (prefilled)')
    assembly_indoor = StringField(label='Assembly (indoor)')
    assembly_outdoor = StringField(label='Assembly (outdoor)')
    harting_plugs = StringField(label='Harting plugs')
    ditec_seals = StringField(label='Ditec seals')
    steel_supp_s = StringField(label='Steel support (small)')
    steel_supp_m = StringField(label='Steel support (medium)')
    steel_supp_l = StringField(label='Steel support (large)')
    drives = StringField(label='Drives')
    core_drilling = StringField(label='Core drillings')
    converter = StringField(label='Converters')
    outdoor_bushing= StringField(label='Outdoor bushings')
    ## general info
    workdays_per_week = IntegerField(label='Workdays per week')
    hours_per_day = IntegerField(label='Hours per day')
    number_of_site_manager = IntegerField(label='Number of site managers')
    number_of_commissioning_engineers = IntegerField(label='Number of commissioning engineers')
    transport_weeks_tools = IntegerField(label='Transport weeks for tools')
    transport_weeks_HVTE = IntegerField(label='Transport weeks for HV-Test equipment')
    arrival_departure_days = IntegerField(label='Arrival and departure days')
    country_factor = IntegerField(label='Country factor')
    customer_training_days = IntegerField(label='Customer training days')

class SaveForm(FlaskForm):
    submit = SubmitField(label='Save project!')

class CostForm(FlaskForm):
    rental_mode_day = SelectField(u'Hours per day', coerce=str)
    rental_mode_week = SelectField(u'Days per week', coerce=str)

class StaffCostForm(FlaskForm):

    service = SelectField(u'Service', coerce=str)
    # unitprice = IntegerField(label='Unit price')
    rentalmode = SelectField(u'Rental mode', coerce=str)
    rentalunits = IntegerField(label='Rental units', validators=[DataRequired()] )
    remark = StringField(label='Remark')

class InstallationToolsCostForm(FlaskForm):

    service = SelectField(u'Service', coerce=str)
    unitprice = IntegerField(label='Unit price')
    rentalmode = SelectField(u'Rental mode', coerce=str)
    rentalunits = IntegerField(label='Rental units')
    remark = StringField(label='Remark')

class ManpowerForm(FlaskForm):
    group_scope_of_work_I = SelectField(u'Group of scope I', coerce=str)
    group_scope_of_work_C = SelectField(u'Group of scope C', coerce=str)
    additional_scope      = StringField(u'Additional scope')
    staff_from_temp       = SelectField(u'staff selector', coerce=str)
    scopes_from_temp      = SelectField(u'scope selector', coerce=str)
    date_start            = DateField(label="Start", format='%Y-%m-%d')#, validators=[DataRequired()])
    date_stop             = DateField(label="Stop", format='%Y-%m-%d')#, validators=[DataRequired()])
    submit                = SubmitField(label='Refresh page')
    rental_mode_day       = SelectField(u'Hours per day', coerce=str)
    rental_mode_week      = SelectField(u'Days per week', coerce=str)
