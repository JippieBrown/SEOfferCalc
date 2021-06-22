from OfferGUI import db, login_manager
from OfferGUI import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __bind_key__ = 'shared'
    id               = db.Column(db.Integer(), primary_key=True)
    username         = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address    = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash    = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class static_costs_commissioning_tools(db.Model):
    __bind_key__ = 'local'
    id          = db.Column(db.Integer(), primary_key=True)
    service     = db.Column(db.String())

class static_costs_installation_tools(db.Model):
    __bind_key__ = 'local'
    id          = db.Column(db.Integer(), primary_key=True)
    service     = db.Column(db.String())

class static_costs_site_equipment(db.Model):
    __bind_key__ = 'local'
    id          = db.Column(db.Integer(), primary_key=True)
    service     = db.Column(db.String())

class static_costs_staff(db.Model):
    __bind_key__ = 'local'
    id                      = db.Column(db.Integer(), primary_key=True)
    service                 = db.Column(db.String())
    price_reg_inquiry_RC    = db.Column(db.String())
    price_reg_inquiry_OE    = db.Column(db.String())
    price_reg_inquiry_RC_DE = db.Column(db.String())

class static_costs_testing_tools(db.Model):
    __bind_key__ = 'local'
    id          = db.Column(db.Integer(), primary_key=True)
    service     = db.Column(db.String())

class static_costs_travel_accommodation(db.Model):
    __bind_key__ = 'local'
    id          = db.Column(db.Integer(), primary_key=True)
    service     = db.Column(db.String())

class static_lead_times(db.Model):
    __bind_key__ = 'local'
    id                   = db.Column(db.Integer(), primary_key=True)
    plant_type           = db.Column(db.String())
    team                 = db.Column(db.String())
    group_scope_of_work  = db.Column(db.String())
    scope_of_work        = db.Column(db.String())
    work_time            = db.Column(db.Integer())
    work_time_unit       = db.Column(db.String())

class gantt(db.Model):
    __bind_key__ = 'local'
    id         = db.Column(db.Integer(), primary_key=True)
    Task       = db.Column(db.String())
    Start      = db.Column(db.String())
    Finish     = db.Column(db.String())
    Resource   = db.Column(db.String())

class temp_planner(db.Model):
    __bind_key__ = 'local'
    id                    = db.Column(db.Integer(), primary_key=True)
    scope                 = db.Column(db.String())    
    staff                 = db.Column(db.String()) 
    start                 = db.Column(db.String())
    stop                  = db.Column(db.String())
    workdays              = db.Column(db.String())

class temp_group_scope_of_work(db.Model):
    __bind_key__ = 'local'
    id                   = db.Column(db.Integer(), primary_key=True)
    team                 = db.Column(db.String())    
    group_scope_of_work  = db.Column(db.String())          

class temp_project_info(db.Model):
    __bind_key__ = 'local'
    ### inquiry info
    id                            = db.Column(db.Integer(), primary_key=True)
    first_name                    = db.Column(db.String())           
    last_name                     = db.Column(db.String())          
    department                    = db.Column(db.String())            
    project_name                  = db.Column(db.String())              
    country                       = db.Column(db.String())         
    city                          = db.Column(db.String())      
    inquiry_date                  = db.Column(db.String())              
    plant_type                    = db.Column(db.String())                
    validity                      = db.Column(db.String())          
    protection_class_indoor       = db.Column(db.String())                         
    protection_class_outdoor      = db.Column(db.String())                          
    calc_for                      = db.Column(db.String())          
    busbar                        = db.Column(db.String())        
    number_of_bays                = db.Column(db.String())                
    supervision                   = db.Column(db.String())             
    commissioning                 = db.Column(db.String())               
    mpd                           = db.Column(db.String())     
    language                      = db.Column(db.String())          
    tools                         = db.Column(db.String())       
    hv_test_equipment             = db.Column(db.String())                   
    transport                     = db.Column(db.String())           
    sec_works                     = db.Column(db.String())           
    sec_works_no_of_bays          = db.Column(db.String())                      
    earthing                      = db.Column(db.String())          
    pd_measurement                = db.Column(db.String())                
    psd                           = db.Column(db.String())     
    actas                         = db.Column(db.String())       
    libo                          = db.Column(db.String())      
    customer_training             = db.Column(db.String())                   
    indoor_crane                  = db.Column(db.String())              
    dc_supply                     = db.Column(db.String())           
    hv_plugs                      = db.Column(db.String())          
    hv_plug_size                  = db.Column(db.String())              
    remark                        = db.Column(db.String())        
    offer_until                   = db.Column(db.String())             
    kick_off_meeting              = db.Column(db.String())                  
    ### project page info
    project_id                    = db.Column(db.String())
    order_indicator               = db.Column(db.String())
    customer                      = db.Column(db.String())
    date_of_editing               = db.Column(db.String())
    editor                        = db.Column(db.String())
    mpd_staff                     = db.Column(db.String())
    mpd_scope_group               = db.Column(db.String())
    mpd_scope_team                = db.Column(db.String())
    mpd_planner_scope             = db.Column(db.String())
    mpd_planner_staff             = db.Column(db.String())
    mpd_planner_start             = db.Column(db.String())
    mpd_planner_stop              = db.Column(db.String())
    mpd_planner_workdays          = db.Column(db.String())
    def __repr__(self):
        return f'project_info {self.name}'   

class temp_staff(db.Model):
    __bind_key__ = 'local'
    id              = db.Column(db.Integer(), primary_key=True)
    Service         = db.Column(db.String(length=30), nullable=False, unique=True)
    UnitPrice       = db.Column(db.Integer(), nullable=False)
    RentalMode      = db.Column(db.String(), nullable=False)
    RentalUnits     = db.Column(db.String(), nullable=False)
    Remark          = db.Column(db.String(length=60), nullable=False)
    Sum             = db.Column(db.Integer(), nullable=False)
    # def __repr__(self):
    #     return f'staff_costs {self.name}'
    
class temp_tool_costs(db.Model):
    __bind_key__ = 'local'
    id              = db.Column(db.Integer(), primary_key=True)
    Service         = db.Column(db.String(length=30), nullable=False, unique=True)
    UnitPrice       = db.Column(db.Integer(), nullable=False)
    RentalMode      = db.Column(db.String(), nullable=False)
    RentalPeriod    = db.Column(db.String(), nullable=False)
    Remark          = db.Column(db.String(length=60), nullable=False)
    Sum             = db.Column(db.Integer(), nullable=False)
    # def __repr__(self):
    #     return f'staff_costs {self.name}'

class dropdown_elements(db.Model):
    __bind_key__ = 'local'
    id                    = db.Column(db.Integer(), primary_key=True)
    plant_type            = db.Column(db.String())
    busbar                = db.Column(db.String())
    calc_for              = db.Column(db.String())
    yes_no                = db.Column(db.String())
    languages             = db.Column(db.String())
    hvt_pd_check          = db.Column(db.String())
    sec_wiring            = db.Column(db.String())
    protect_class_indoor  = db.Column(db.String())
    protect_class_outdoor = db.Column(db.String())
    rental_mode           = db.Column(db.String())
    rental_mode_day       = db.Column(db.String())
    rental_mode_week      = db.Column(db.String())
    hv_plugs              = db.Column(db.String())
    hv_plug_size          = db.Column(db.String())
    actas                 = db.Column(db.String())
    years                 = db.Column(db.String())  
    # def __repr__(self):
    #     return f'dropdown_elements {self.name}'

class collected_projects(db.Model):
    __bind_key__ = 'shared'
    ### inquiry info
    id                            = db.Column(db.Integer(), primary_key=True)    
    first_name                    = db.Column(db.String())           
    last_name                     = db.Column(db.String())          
    department                    = db.Column(db.String())            
    project_name                  = db.Column(db.String(), unique=True)              
    country                       = db.Column(db.String())         
    city                          = db.Column(db.String())      
    inquiry_date                  = db.Column(db.String())              
    plant_type                    = db.Column(db.String())                
    validity                      = db.Column(db.String())          
    protection_class_indoor       = db.Column(db.String())                         
    protection_class_outdoor      = db.Column(db.String())                          
    calc_for                      = db.Column(db.String())          
    busbar                        = db.Column(db.String())        
    number_of_bays                = db.Column(db.String())                
    supervision                   = db.Column(db.String())             
    commissioning                 = db.Column(db.String())               
    mpd                           = db.Column(db.String())     
    language                      = db.Column(db.String())          
    tools                         = db.Column(db.String())       
    hv_test_equipment             = db.Column(db.String())                   
    transport                     = db.Column(db.String())           
    sec_works                     = db.Column(db.String())           
    sec_works_no_of_bays          = db.Column(db.String())                      
    earthing                      = db.Column(db.String())          
    pd_measurement                = db.Column(db.String())                
    psd                           = db.Column(db.String())     
    actas                         = db.Column(db.String())       
    libo                          = db.Column(db.String())      
    customer_training             = db.Column(db.String())                   
    indoor_crane                  = db.Column(db.String())              
    dc_supply                     = db.Column(db.String())           
    hv_plugs                      = db.Column(db.String())          
    hv_plug_size                  = db.Column(db.String())              
    remark                        = db.Column(db.String())        
    offer_until                   = db.Column(db.String())             
    kick_off_meeting              = db.Column(db.String())                  
    ### project page info
    project_id                    = db.Column(db.String(), unique=True)
    order_indicator               = db.Column(db.String())
    customer                      = db.Column(db.String())
    date_of_editing               = db.Column(db.String())
    editor                        = db.Column(db.String())
    ### Manpower page 
    mpd_staff                     = db.Column(db.String())
    mpd_scope_group               = db.Column(db.String())
    mpd_scope_team                = db.Column(db.String())
    mpd_planner_scope             = db.Column(db.String())
    mpd_planner_staff             = db.Column(db.String())
    mpd_planner_start             = db.Column(db.String())
    mpd_planner_stop              = db.Column(db.String())
    mpd_planner_workdays          = db.Column(db.String())

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
    def __repr__(self):
        return f'project_info {self.name}'   

class MOS_dropdown_elements(db.Model):
    __bind_key__ = 'MOS'
    id                    = db.Column(db.Integer(), primary_key=True)
    plant_type            = db.Column(db.String())
    yes_no                = db.Column(db.String())
    language              = db.Column(db.String())
    pdm_type              = db.Column(db.String())
