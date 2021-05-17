from OfferGUI import app, db
from OfferGUI.models import *
from OfferGUI.forms import *
from flask import render_template, redirect, request, url_for, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from OfferGUI.tools import AddRow, DelRow, XmlReader, RemoveTemporaryItems, SelectFieldSetter
import os
import xmltodict
@app.route('/costs', methods=['POST', 'GET'])
@login_required
def costs_page():
    if len(temp_project_info.query.all()) == 0:
       flash(f"No project selected!", category='info')
       return redirect(url_for('home_page'))  
    # if len(temp_project_info.query.all()) == 0:
    #     flash(f"No project selected!", category='info')
    #     return redirect(url_for('home_page'))  
    # project_info = 
    staff_form = StaffCostForm()
    install_form = InstallationToolsCostForm()
    sc = temp_staff_costs
    stat_c_s = static_costs_staff
    stat_c_it = static_costs_installation_tools
    # class from from models-py
    dde = dropdown_elements
    #reading dropdown choices from database
    db_static_staff = stat_c_s.query.with_entities(stat_c_s.service, 
                                                   stat_c_s.service).filter(
                                                   stat_c_s.service!="NULL")
    db_static_rentalmode = dde.query.with_entities(dde.rental_mode, 
                                                   dde.rental_mode).filter(
                                                   dde.rental_mode!="NULL")    
    db_static_installation = stat_c_it.query.with_entities(stat_c_it.service, 
                                                           stat_c_it.service).filter(
                                                           stat_c_it.service!="NULL")  

    #reading table data from database
    staff_items = temp_staff_costs.query.all()
    tool_items = temp_tool_costs.query.all()
    project_info_items = temp_project_info.query.all()

    #select items by column name
    temp_calc_for = [k.calc_for for k in project_info_items]
    temp_sum_total = sum([k.Sum for k in staff_items])
    # print(temp_calc_for)
    # print(temp_sum)

    #setting choices
    staff_form.service.choices = [k for k in db_static_staff]
    staff_form.rentalmode.choices = [k for k in db_static_rentalmode]
    install_form.service.choices = [k for k in db_static_installation]



    # if temp_calc_for == ['RC']:
    #     print(temp_calc_for)

    if request.method == 'POST':
        if request.form.get('StaffCostPlusBtn'):
            staff_cost_output = [request.form[key] for key in request.form.keys()]
            # print(staff_cost_output)
            staff_form.service.data = staff_cost_output[1]
            staff_price_row = stat_c_s.query.filter_by(service=staff_cost_output[1]).first()
            if temp_calc_for == ['RC']:
                staff_price_item = staff_price_row.price_reg_inquiry_RC
                # print(staff_price_item)
            elif temp_calc_for == ['PRO GIS']:
                staff_price_item = staff_price_row.price_reg_inquiry_OE
                # print(staff_price_item)
            elif temp_calc_for == ['DE TM']:
                staff_price_item = staff_price_row.price_reg_inquiry_RC_DE
            # print(int(staff_price_item)*int(staff_cost_output[2]))                                
            sum_staff_item = int(staff_price_item)*int(staff_cost_output[2])
            staff_form.rentalmode.data = staff_cost_output[3]
            staff_form.rentalunits.data = staff_cost_output[2]
            staff_form.remark.data = staff_cost_output[4]
            if int(staff_form.rentalunits.data) > 0:
                AddRow(temp_staff_costs, staff_cost_output, staff_price_item, sum_staff_item)
            else:
                flash(f"Rental unit must be greater than zero", category='danger')

        elif request.form.get('StaffCostMinusBtn'): 
            # print(request.form.get('StaffCostMinusBtn'))    
            DelRow(temp_staff_costs,int(request.form.get('StaffCostMinusBtn')))
        elif request.form.get('ToolCostPlusBtn'):
            AddRow(temp_tool_costs)
        elif request.form.get('ToolCostMinusBtn'):
            DelRow(temp_tool_costs)        
        return redirect(url_for('costs_page'))
    
    return render_template('costs.html', staff_form=staff_form, 
                                         install_form=install_form, 
                                         staff_items=staff_items, 
                                         tool_items=tool_items,
                                         project_info_items=project_info_items,
                                         temp_sum_total=temp_sum_total)

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    RemoveTemporaryItems()
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'User and/or Password wrong! Try again', category='success')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    RemoveTemporaryItems()
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    home_form = HomeForm()
    db_projects = collected_projects.query.with_entities(collected_projects.project_name, collected_projects.project_name).filter(collected_projects.project_name!="NULL")
    home_form.project.choices = [k for k in db_projects]
    if request.method == 'POST':
        if request.form.get('LoadExistingProject'):
            RemoveTemporaryItems()
            # print("removed!")
            req_project_name = [request.form[key] for key in request.form.keys()][1]
            ### get row in collected projects by select field above 'load'
            project_row = collected_projects.query.filter_by(project_name=req_project_name).first()
            # print(project_row.id)

            ### writing in database
            temp_project_infos = temp_project_info(first_name               = project_row.first_name               ,
                                                   last_name                = project_row.last_name                ,
                                                   department               = project_row.department               ,
                                                   project_name             = project_row.project_name             ,
                                                   country                  = project_row.country                  ,
                                                   city                     = project_row.city                     ,
                                                   inquiry_date             = project_row.inquiry_date             ,
                                                   plant_type               = project_row.plant_type               ,
                                                   validity                 = project_row.validity                 ,
                                                   protection_class_indoor  = project_row.protection_class_indoor  ,
                                                   protection_class_outdoor = project_row.protection_class_outdoor ,
                                                   calc_for                 = project_row.calc_for                 ,
                                                   busbar                   = project_row.busbar                   ,
                                                   number_of_bays           = project_row.number_of_bays           ,
                                                   supervision              = project_row.supervision              ,
                                                   commissioning            = project_row.commissioning            ,
                                                   mpd                      = project_row.mpd                      ,
                                                   language                 = project_row.language                 ,
                                                   tools                    = project_row.tools                    ,
                                                   hv_test_equipment        = project_row.hv_test_equipment        ,
                                                   transport                = project_row.transport                ,
                                                   sec_works                = project_row.sec_works                ,
                                                   sec_works_no_of_bays     = project_row.sec_works_no_of_bays     ,
                                                   earthing                 = project_row.earthing                 ,
                                                   pd_measurement           = project_row.pd_measurement           ,
                                                   psd                      = project_row.psd                      ,
                                                   actas                    = project_row.actas                    ,
                                                   libo                     = project_row.libo                     ,
                                                   customer_training        = project_row.customer_training        ,
                                                   indoor_crane             = project_row.indoor_crane             ,
                                                   dc_supply                = project_row.dc_supply                ,
                                                   hv_plugs                 = project_row.hv_plugs                 ,
                                                   hv_plug_size             = project_row.hv_plug_size             ,
                                                   remark                   = project_row.remark                   ,
                                                   offer_until              = project_row.offer_until              ,
                                                   kick_off_meeting         = project_row.kick_off_meeting         )
                         
            db.session.add(temp_project_infos)
            db.session.commit()
            return redirect(url_for('project_page'))
    return render_template('home.html', home_form=home_form)

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # print(f.filename)
        if f.filename != "":
            f.save(os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename)))
            filepath = os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename))
            #call function
            XmlReader(filepath)
            return redirect(url_for('project_page'))
        else:
            flash(f"Please select file!", category='warning')
            return redirect(url_for('home_page'))

@app.route('/project', methods=['GET', 'POST'])
@login_required
def project_page():
    save_form = SaveForm()
    form = ProjectForm()
    if request.method == 'GET':
        # class from from models-py (shortening)
        dde = dropdown_elements
        # reading from database
        db_user                  = User.query.with_entities(User.username, User.username).all()
        db_plant_type            = dde.query.with_entities(dde.plant_type, dde.plant_type).filter(dde.plant_type!="NULL")
        db_busbar                = dde.query.with_entities(dde.busbar, dde.busbar).filter(dde.busbar!="NULL")
        db_calc_for              = dde.query.with_entities(dde.calc_for, dde.calc_for).filter(dde.calc_for!="NULL")
        db_yes_no                = dde.query.with_entities(dde.yes_no, dde.yes_no).filter(dde.yes_no!="NULL")
        db_languages             = dde.query.with_entities(dde.languages, dde.languages).filter(dde.languages!="NULL")
        db_hvt_pd_check          = dde.query.with_entities(dde.hvt_pd_check, dde.hvt_pd_check).filter(dde.hvt_pd_check!="NULL")        
        db_sec_wiring            = dde.query.with_entities(dde.sec_wiring, dde.sec_wiring).filter(dde.sec_wiring!="NULL")      
        db_protect_class_indoor  = dde.query.with_entities(dde.protect_class_indoor, dde.protect_class_indoor).filter(dde.protect_class_indoor!="NULL")                
        db_protect_class_outdoor = dde.query.with_entities(dde.protect_class_outdoor, dde.protect_class_outdoor).filter(dde.protect_class_outdoor!="NULL")                 
        db_rental_mode           = dde.query.with_entities(dde.rental_mode, dde.rental_mode).filter(dde.rental_mode!="NULL")       
        db_hv_plugs              = dde.query.with_entities(dde.hv_plugs, dde.hv_plugs).filter(dde.hv_plugs!="NULL")    
        db_hv_plug_size          = dde.query.with_entities(dde.hv_plug_size, dde.hv_plug_size).filter(dde.hv_plug_size!="NULL")        
        db_actas                 = dde.query.with_entities(dde.actas, dde.actas).filter(dde.actas!="NULL") 

        # setting choices (forms.py --> class ProjectForm)
        form.editor.choices                   = [k for k in db_user]
        form.plant_type.choices               = [k for k in db_plant_type]
        form.protection_class_indoor.choices  = [k for k in db_protect_class_indoor]
        form.protection_class_outdoor.choices = [k for k in db_protect_class_outdoor]
        form.calc_for.choices                 = [k for k in db_calc_for]
        form.busbar.choices                   = [k for k in db_busbar]
        form.supervision.choices              = [k for k in db_yes_no]
        form.commissioning.choices            = [k for k in db_yes_no]
        form.mpd.choices                      = [k for k in db_yes_no]
        form.language.choices                 = [k for k in db_languages]
        form.tools.choices                    = [k for k in db_yes_no]
        form.hv_test_equipment.choices        = [k for k in db_hvt_pd_check]
        form.transport.choices                = [k for k in db_yes_no]
        form.sec_works.choices                = [k for k in db_sec_wiring]
        form.earthing.choices                 = [k for k in db_yes_no]
        form.pd_measurement.choices           = [k for k in db_yes_no]
        form.psd.choices                      = [k for k in db_yes_no]
        form.actas.choices                    = [k for k in db_actas]
        form.libo.choices                     = [k for k in db_yes_no]
        form.customer_training.choices        = [k for k in db_yes_no]
        form.indoor_crane.choices             = [k for k in db_yes_no]
        form.dc_supply.choices                = [k for k in db_yes_no]
        form.hv_plugs.choices                 = [k for k in db_hv_plugs]
        form.hv_plug_size.choices             = [k for k in db_hv_plug_size]
        #pre setting
        form.gascomp_empty.data = "---not used---"
        form.gascomp_pref.data = "---not used---"
        form.assembly_indoor.data = "---not used---"
        form.assembly_outdoor.data = "---not used---"
        form.harting_plugs.data = "---not used---"
        form.ditec_seals.data = "---not used---"
        form.steel_supp_s.data = "---not used---"
        form.steel_supp_m.data = "---not used---"
        form.steel_supp_l.data = "---not used---"
        form.drives.data = "---not used---"
        form.core_drilling.data = "---not used---"
        form.converter.data = "---not used---"
        form.outdoor_bushing.data = "---not used---"
        form.workdays_per_week.data = "---not used---"
        form.hours_per_day.data = "---not used---"
        form.number_of_site_manager.data = "---not used---"
        form.number_of_commissioning_engineers.data = "---not used---"
        form.transport_weeks_tools.data = "---not used---"
        form.transport_weeks_HVTE.data = "---not used---"
        form.arrival_departure_days.data = "---not used---"
        form.country_factor.data = "---not used---"
        form.customer_training_days.data = "---not used---"

        if len(temp_project_info.query.all()) == 1:
            item = temp_project_info.query.get(1)
            print(item.project_name)
            form.first_name.data               = item.first_name               
            form.last_name.data                = item.last_name                
            form.department.data               = item.department               
            form.project_name.data             = item.project_name             
            form.country.data                  = item.country                  
            form.city.data                     = item.city                     
            if item.inquiry_date != None:
                form.inquiry_date.data             = datetime.strptime(item.inquiry_date, '%Y-%m-%d')              
            form.plant_type.data               = item.plant_type               
            form.validity.data                 = item.validity                 
            form.protection_class_indoor.data  = item.protection_class_indoor  
            form.protection_class_outdoor.data = item.protection_class_outdoor 
            form.calc_for.data                 = item.calc_for                 
            form.busbar.data                   = item.busbar                   
            form.number_of_bays.data           = item.number_of_bays           
            form.supervision.data              = item.supervision              
            form.commissioning.data            = item.commissioning            
            form.mpd.data                      = item.mpd                      
            form.language.data                 = item.language                 
            form.tools.data                    = item.tools                    
            form.hv_test_equipment.data        = item.hv_test_equipment        
            form.transport.data                = item.transport                
            form.sec_works.data                = item.sec_works                
            form.sec_works_no_of_bays.data     = item.sec_works_no_of_bays     
            form.earthing.data                 = item.earthing                 
            form.pd_measurement.data           = item.pd_measurement           
            form.psd.data                      = item.psd                      
            form.actas.data                    = item.actas                    
            form.libo.data                     = item.libo                     
            form.customer_training.data        = item.customer_training        
            form.indoor_crane.data             = item.indoor_crane             
            form.dc_supply.data                = item.dc_supply                
            form.hv_plugs.data                 = item.hv_plugs                 
            form.hv_plug_size.data             = item.hv_plug_size             
            form.remark.data                   = item.remark  
            if item.offer_until != None:                 
                form.offer_until.data              = datetime.strptime(item.offer_until, '%Y-%m-%d')               
            if item.kick_off_meeting != None:
                form.kick_off_meeting.data         = datetime.strptime(item.kick_off_meeting, '%Y-%m-%d')          
            #set data on project info page
            form.project_id.data               = item.project_id      
            form.order_indicator.data          = item.order_indicator              
            form.customer.data                 = item.customer      
            if item.offer_date != None:
                form.offer_date.data           = datetime.strptime(item.offer_date, '%Y-%m-%d')    
            form.editor.data                   = item.editor       

        elif len(temp_project_info.query.all()) == 0:
            flash(f"No project selected!", category='info')
            return redirect(url_for('home_page'))  
    # return render_template('project_info.html', form=form, save_form=save_form)

    if save_form.validate_on_submit():
        # project_output reads content of fields in project_info.html
        project_output = request.form
        print(project_output['project_name'])
        if len(project_output) >= 1:
            # writing in databas
            temp_project_infos = temp_project_info(first_name               = project_output['first_name'] ,
                                                   last_name                = project_output['last_name'] ,
                                                   department               = project_output['department'] ,
                                                   project_name             = project_output['project_name'] ,
                                                   country                  = project_output['country'] ,
                                                   city                     = project_output['city'] ,
                                                   inquiry_date             = project_output['inquiry_date'] ,
                                                   plant_type               = project_output['plant_type'] ,
                                                   validity                 = project_output['validity'] ,
                                                   protection_class_indoor  = project_output['protection_class_indoor'] ,
                                                   protection_class_outdoor = project_output['protection_class_outdoor'] ,
                                                   calc_for                 = project_output['calc_for'] ,
                                                   busbar                   = project_output['busbar'] ,
                                                   number_of_bays           = project_output['number_of_bays'] ,
                                                   supervision              = project_output['supervision'] ,
                                                   commissioning            = project_output['commissioning'] ,
                                                   mpd                      = project_output['mpd'] ,
                                                   language                 = project_output['language'] ,
                                                   tools                    = project_output['tools'] ,
                                                   hv_test_equipment        = project_output['hv_test_equipment'] ,
                                                   transport                = project_output['transport'] ,
                                                   sec_works                = project_output['sec_works'] ,
                                                   sec_works_no_of_bays     = project_output['sec_works_no_of_bays'] ,
                                                   earthing                 = project_output['earthing'] ,
                                                   pd_measurement           = project_output['pd_measurement'] ,
                                                   psd                      = project_output['psd'] ,
                                                   actas                    = project_output['actas'] ,
                                                   libo                     = project_output['libo'] ,
                                                   customer_training        = project_output['customer_training'] ,
                                                   indoor_crane             = project_output['indoor_crane'] ,
                                                   dc_supply                = project_output['dc_supply'] ,
                                                   hv_plugs                 = project_output['hv_plugs'] ,
                                                   hv_plug_size             = project_output['hv_plug_size'] ,
                                                   remark                   = project_output['remark'] ,
                                                   offer_until              = project_output['offer_until'] ,
                                                   kick_off_meeting         = project_output['kick_off_meeting'] ,
                                                   order_indicator          = project_output['order_indicator'] ,
                                                   customer                 = project_output['customer'] ,
                                                   project_id               = project_output['project_id'] )
            ### Overwrite existing project
            project_row = collected_projects.query.filter_by(project_name=project_output['project_name']).first()
            # print(project_row)  
            if project_row != None:
                db.session.delete(collected_projects.query.get(project_row.id))
            # db.session.commit()
            temp_project_info.query.delete()
            db.session.commit()
            # db.session.add(project_infos)
            db.session.add(temp_project_infos)
            
            db.session.commit()
            flash(f"Data from project page stored in database!", category='success')
        return redirect(url_for('costs_page'))
    return render_template('project_info.html', form=form, save_form=save_form)

@app.route('/manpower', methods = ['GET', 'POST'])
def manpower_page():
    if len(temp_project_info.query.all()) == 0:
       flash(f"No project selected!", category='info')
       return redirect(url_for('home_page'))      
    return render_template('manpower_calc.html')
