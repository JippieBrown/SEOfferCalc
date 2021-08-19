from OfferGUI import app, db
from OfferGUI.models import *
from OfferGUI.forms import *
from flask import render_template, redirect, request, url_for, flash, get_flashed_messages, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from networkdays import networkdays
from OfferGUI.tools import AddRow, DelRow, XmlReader, RemoveTemporaryItems
import os
import xmltodict
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import plotly.io as pio
from ast import literal_eval
import workdays as workdays

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    home_form = HomeForm()
    db_projects = collected_projects.query.with_entities(collected_projects.project_name, collected_projects.project_name).filter(collected_projects.project_name!="NULL")
    home_form.project.choices = [k for k in db_projects]
    if request.method == 'POST':
        if request.form.get('LoadExistingProject'):
        ### Clear temp 
            RemoveTemporaryItems()
        ### get row in collected projects by select field above 'load'
            req_project_name = [request.form[key] for key in request.form.keys()][1]
            project_row = collected_projects.query.filter_by(project_name=req_project_name).first()
            # print(project_row.id)

        ### data from collected projects into temp projects
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
                                                   kick_off_meeting         = project_row.kick_off_meeting         ,
                                                   order_indicator          = project_row.order_indicator          ,
                                                   customer                 = project_row.customer                 ,
                                                   project_id               = project_row.project_id               ,
                                                   editor                   = project_row.editor                   ,
                                                   date_of_editing          = project_row.date_of_editing          ,
                                                   mpd_staff                = project_row.mpd_staff                ,
                                                   mpd_scope_group          = project_row.mpd_scope_group          ,
                                                   mpd_scope_team           = project_row.mpd_scope_team           ,
                                                   mpd_planner_scope        = project_row.mpd_planner_scope        , 
                                                   mpd_planner_staff        = project_row.mpd_planner_staff        , 
                                                   mpd_planner_start        = project_row.mpd_planner_start        , 
                                                   mpd_planner_stop         = project_row.mpd_planner_stop         ,
                                                   mpd_planner_workdays     = project_row.mpd_planner_workdays     )          
                                                   
            db.session.add(temp_project_infos)
            db.session.commit()

        ### data from collected projects into temp staff
            if project_row.mpd_staff != None:
                for k in literal_eval(project_row.mpd_staff):
                    db.session.add(temp_staff(Service = k))
                db.session.commit()

        ### data from collected projects into temp group scope of work
            if project_row.mpd_scope_group != None:
                for k,l in zip(literal_eval(project_row.mpd_scope_group),literal_eval(project_row.mpd_scope_team)):
                    db.session.add(temp_group_scope_of_work(group_scope_of_work = k,
                                                            team = l))
                db.session.commit()

        ### data from collected projects into temp planner
            if project_row.mpd_planner_scope != None:
                for k,l,m,n,o in zip(literal_eval(project_row.mpd_planner_scope),
                                   literal_eval(project_row.mpd_planner_staff),
                                   literal_eval(project_row.mpd_planner_start),
                                   literal_eval(project_row.mpd_planner_stop),
                                   literal_eval(project_row.mpd_planner_workdays)):
                    db.session.add(temp_planner(scope = k,
                                                staff = l,
                                                start = m,
                                                stop = n,
                                                workdays = o))
                db.session.commit()                

        ### return
            return redirect(url_for('project_page'))

    ### Testing the printer view ----TODO------
        if request.form.get('CreateMethodStatement'):              
            return redirect(url_for('methodstatement')) 
    
    return render_template('home.html', home_form=home_form)

@app.route('/methodstatement', methods = ['GET','POST'])
def methodstatement():
    project_info_items = temp_project_info.query.all()
    return render_template('methodstatement.html', 
                                                   project_info_items=project_info_items)

@app.route("/update_planner",methods=["POST","GET"])
def update_planner():
    if request.method == 'POST':
        if request.form.get('test'):
            print(request.form)
            print('LOL geht')
        
    return redirect(url_for('manpower_page'))
    # try:
    #     conn = mysql.connect()
    #     cursor = conn.cursor(pymysql.cursors.DictCursor)
    #     if request.method == 'POST':
    #         field = request.form['field'] 
    #         value = request.form['value']
    #         editid = request.form['id']
             
    #         if field == 'username':
    #            sql = "UPDATE users SET username=%s WHERE id=%s"
    #         if field == 'name':        
    #             sql = "UPDATE users SET name=%s WHERE id=%s"
 
    #         data = (value, editid)
    #         conn = mysql.connect()
    #         cursor = conn.cursor()
    #         cursor.execute(sql, data)
    #         conn.commit()
    #         success = 1
    #     return jsonify(success)
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close() 
    #     conn.close()


@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename)))
            filepath = os.path.join(app.config['UPLOAD_PATH'],secure_filename(f.filename))
            #call function
            XmlReader(filepath)
            return redirect(url_for('project_page'))
        except:
            flash(f"Please select file!", category='warning')
            return redirect(url_for('home_page'))

@app.route('/project', methods=['GET', 'POST'])
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
        db_validity              = dde.query.with_entities(dde.years, dde.years).filter(dde.years!="NULL") 
        # setting choices (forms.py --> class ProjectForm)
        form.editor.choices                   = [k for k in db_user]
        form.plant_type.choices               = [k for k in db_plant_type]
        form.protection_class_indoor.choices  = [k for k in db_protect_class_indoor]
        form.protection_class_outdoor.choices = [k for k in db_protect_class_outdoor]
        form.calc_for.choices                 = [k for k in db_calc_for]
        form.validity.choices                 = [k for k in db_validity]
        form.busbar.choices                   = [k for k in db_busbar]
        form.supervision.choices              = [k for k in db_yes_no]
        form.commissioning.choices            = [k for k in db_yes_no]
        form.mpd.choices                      = [k for k in db_yes_no]
        form.language.choices                 = [k for k in db_languages]
        form.tools.choices                    = [k for k in db_yes_no]
        form.hv_test_equipment.choices        = [k for k in db_yes_no]
        form.transport.choices                = [k for k in db_yes_no]
        form.sec_works.choices                = [k for k in db_sec_wiring]
        form.earthing.choices                 = [k for k in db_yes_no]
        form.pd_measurement.choices           = [k for k in db_hvt_pd_check]
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
            # print(item.project_name)
            form.first_name.data               = item.first_name               
            form.last_name.data                = item.last_name                
            form.department.data               = item.department               
            form.project_name.data             = item.project_name             
            form.country.data                  = item.country                  
            form.city.data                     = item.city                     
            if item.inquiry_date != None and item.inquiry_date != "":
                form.inquiry_date.data             = datetime.strptime(item.inquiry_date, '%Y-%m-%d')              
            form.plant_type.data               = item.plant_type
            if item.validity != None and item.validity != "":              
                form.validity.data                 = datetime.strptime(item.validity , '%Y')                
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
            if item.offer_until != None and item.offer_until != "":                 
                form.offer_until.data              = datetime.strptime(item.offer_until, '%Y-%m-%d')               
            if item.kick_off_meeting != None and item.kick_off_meeting != "":
                form.kick_off_meeting.data         = datetime.strptime(item.kick_off_meeting, '%Y-%m-%d')          
            #set data on project info page
            form.project_id.data               = item.project_id      
            form.order_indicator.data          = item.order_indicator              
            form.customer.data                 = item.customer      
            if item.date_of_editing != None and item.date_of_editing != "":
                form.date_of_editing.data           = datetime.strptime(str(date.today()), '%Y-%m-%d')    
            form.editor.data                   = item.editor       

        elif len(temp_project_info.query.all()) == 0:
            flash(f"No project selected!", category='info')
            return redirect(url_for('home_page'))  

    if save_form.validate_on_submit():
        # project_output reads content of fields in project_info.html
        project_output = request.form

        # print(project_output)
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
                                                   project_id               = project_output['project_id'],
                                                   editor                   = current_user.username,
                                                   date_of_editing          = project_output['date_of_editing'] )

            project_infos = collected_projects(first_name               = project_output['first_name'] ,
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
                                               project_id               = project_output['project_id'],
                                               editor                   = current_user.username,
                                               date_of_editing          = project_output['date_of_editing'] )            


            ### Overwrite existing project
            project_row_name = collected_projects.query.filter_by(project_name=project_output['project_name']).first()
            project_row_project_id= collected_projects.query.filter_by(project_id=project_output['project_id']).first()


            if project_row_name != None and project_row_project_id != None:
                db.session.delete(collected_projects.query.get(project_row_name.id))
                temp_project_info.query.delete()
                db.session.commit()
                db.session.add(project_infos)
                db.session.add(temp_project_infos)
                db.session.commit()
                flash(f"Data overwritten in database!", category='success')
                return redirect(url_for('manpower_page'))
            elif project_row_name == None and project_row_project_id != None:
                temp_project_info.query.delete()
                db.session.commit()
                db.session.add(temp_project_infos)
                db.session.commit()
                flash(f"Change Project ID!", category='danger')
                return redirect(url_for('project_page'))
            elif project_row_name == None and project_row_project_id == None: 
                temp_project_info.query.delete()
                db.session.commit()
                db.session.add(project_infos)
                db.session.add(temp_project_infos)
                db.session.commit()
                flash(f"Data from project page stored in database!", category='success')
                return redirect(url_for('manpower_page'))     
    return render_template('project_info.html', form=form, save_form=save_form)

@app.route('/manpower', methods = ['GET', 'POST'])
def manpower_page():
 ### Flashes
    if len(temp_project_info.query.all()) == 0:
        flash(f"No project selected!", category='info')
        return redirect(url_for('home_page'))

 ### Setting variables
    slt = static_lead_times
    stat_c_s = static_costs_staff
    dde = dropdown_elements
    staff_form = StaffCostForm()
    manpower_form = ManpowerForm()
    save_form = SaveForm()

 ### Reading table data from database
    temp_group_scope_of_work_items = temp_group_scope_of_work.query.all()
    project_info_items = temp_project_info.query.all()
    temp_planner_items = temp_planner.query.all()
    staff_items = temp_staff.query.all()

    db_static_rentalmode_day = dde.query.with_entities(dde.rental_mode_day, 
                                                   dde.rental_mode_day).filter(
                                                   dde.rental_mode_day!="NULL")

    db_static_rentalmode_week = dde.query.with_entities(dde.rental_mode_week, 
                                                   dde.rental_mode_week).filter(
                                                   dde.rental_mode_week!="NULL") 
                                                   
    db_static_staff = stat_c_s.query.with_entities(stat_c_s.service, 
                                                   stat_c_s.service).filter(
                                                   stat_c_s.service!="NULL")
    db_group_scope_I = slt.query.with_entities(slt.group_scope_of_work, 
                                               slt.group_scope_of_work).filter(
                                               slt.group_scope_of_work!="NULL" and slt.team=="Supervisor")

    db_group_scope_C = slt.query.with_entities(slt.group_scope_of_work, 
                                               slt.group_scope_of_work).filter(
                                               slt.group_scope_of_work!="NULL" and slt.team=="Commissioning Engineer")

    db_temp_group_scope_of_work_items = temp_group_scope_of_work.query.with_entities(
                                        temp_group_scope_of_work.group_scope_of_work, 
                                        temp_group_scope_of_work.group_scope_of_work).filter(
                                        temp_group_scope_of_work.group_scope_of_work!="NULL")

 ### Unplanned scopes
    '''Fill the list missing_scopes by substracting chosen scopes from planned scopes'''                                    
    unplanned_scopes = [k for k in [i.group_scope_of_work for i in db_temp_group_scope_of_work_items] if 
                                k not in [j.scope for j in temp_planner_items]]
    # print(missing_scopes)

 ### Setting choices   
    manpower_form.rental_mode_day.choices = [k for k in db_static_rentalmode_day]
    manpower_form.rental_mode_week.choices = [k for k in db_static_rentalmode_week]                              
    staff_form.service.choices = [k for k in db_static_staff]   
    manpower_form.group_scope_of_work_I.choices = []
    manpower_form.group_scope_of_work_C.choices = []
    manpower_form.staff_from_temp.choices = [k.Service + " / ID " + str(k.id) for k in staff_items]
    manpower_form.scopes_from_temp.choices = [k for k in db_temp_group_scope_of_work_items]
    [manpower_form.group_scope_of_work_I.choices.append(k) for k in db_group_scope_I if 
                                                                    k not in manpower_form.group_scope_of_work_I.choices and 
                                                                    k not in db_temp_group_scope_of_work_items]
    [manpower_form.group_scope_of_work_C.choices.append(k) for k in db_group_scope_C if 
                                                                    k not in manpower_form.group_scope_of_work_C.choices and 
                                                                    k not in db_temp_group_scope_of_work_items]
    manpower_form.date_start.data = datetime.today()
    # print(manpower_form.date_start.data)
    manpower_form.date_stop.data = datetime.today() + timedelta(days=1)

 ### POST actions
    if request.method == 'POST':

    ### Rental mode
        if request.form.get('rental_mode_day'):
            print(request.form)
        # if save_form.validate_on_submit():    
        #     print('LOL')
        
    ### Save
        if request.form.get('Save'):
            print(request.form)
            temp_project = temp_project_info.query.get(1)
            temp_project.mpd_staff = str([(k.Service + " / ID " + str(k.id)) for k in staff_items])
            temp_project.mpd_scope_group = str([k.group_scope_of_work for k in temp_group_scope_of_work_items])
            temp_project.mpd_scope_team = str([k.team for k in temp_group_scope_of_work_items])
            temp_project.mpd_planner_scope= str([k.scope for k in temp_planner_items])
            temp_project.mpd_planner_staff = str([k.staff for k in temp_planner_items])
            temp_project.mpd_planner_start = str([k.start for k in temp_planner_items])
            temp_project.mpd_planner_stop = str([k.stop for k in temp_planner_items])
            temp_project.mpd_planner_workdays = str([k.workdays for k in temp_planner_items])

            search_id_active_collected_project = collected_projects.query.filter_by(project_name=temp_project.project_name).first().id
            active_collected_projects = collected_projects.query.get(search_id_active_collected_project)
            active_collected_projects.mpd_staff = str([(k.Service) for k in staff_items])
            active_collected_projects.mpd_scope_group = str([k.group_scope_of_work for k in temp_group_scope_of_work_items])
            active_collected_projects.mpd_scope_team = str([k.team for k in temp_group_scope_of_work_items])
            active_collected_projects.mpd_planner_scope = str([k.scope for k in temp_planner_items])
            active_collected_projects.mpd_planner_staff = str([k.staff for k in temp_planner_items])
            active_collected_projects.mpd_planner_start = str([k.start for k in temp_planner_items])
            active_collected_projects.mpd_planner_stop = str([k.stop for k in temp_planner_items])
            active_collected_projects.mpd_planner_workdays = str([k.workdays for k in temp_planner_items])            
            db.session.commit()
            # print([k.Service + " / ID " + str(k.id) for k in staff_items])
            flash(f"Data overwritten in database!", category='success')
        
    ### Staff
        if request.form.get('StaffCostPlusBtn'):
            staff_cost_output = request.form
            staff_form.service.data = staff_cost_output['service']
            if 'service' in staff_cost_output:
                db.session.add(temp_staff(Service = staff_cost_output['service']))
                temp_project = temp_project_info.query.get(1)
                temp_project.mpd_staff = str([(k.Service + " / ID " + str(k.id)) for k in temp_staff.query.all()])
                db.session.commit()
            return redirect(url_for('manpower_page'))
        if request.form.get('StaffCostMinusBtn'): 
            DelRow(temp_staff,int(request.form.get('StaffCostMinusBtn')))
            temp_project = temp_project_info.query.get(1)
            temp_project.mpd_staff = str([(k.Service + " / ID " + str(k.id)) for k in temp_staff.query.all()])
            db.session.commit()
            return redirect(url_for('manpower_page'))

    ### Installation scopes
        if request.form.get('InstallationScopePlusBtn'):
            scope_of_work_output = request.form
            if 'group_scope_of_work_I' in scope_of_work_output:
                db.session.add(temp_group_scope_of_work(group_scope_of_work = scope_of_work_output['group_scope_of_work_I'],
                                                        team                = "Supervisor"))
                db.session.commit()
            else:
                flash(f"No scopes available!", category='warning')
            return redirect(url_for('manpower_page'))
        if request.form.get('InstallationScopeMinusBtn'):
            DelRow(temp_group_scope_of_work, int(request.form.get('InstallationScopeMinusBtn')))
            return redirect(url_for('manpower_page'))

    ### Commissioning scopes
        if request.form.get('CommissioningScopePlusBtn'):
            scope_of_work_output = request.form
            if 'group_scope_of_work_C' in scope_of_work_output:
                db.session.add(temp_group_scope_of_work(group_scope_of_work = scope_of_work_output['group_scope_of_work_C'],
                                                        team                = "Commissioning Engineer"))
                db.session.commit()
            else:
                flash(f"No scopes available!", category='warning')
            return redirect(url_for('manpower_page'))
        if request.form.get('CommissioningScopeMinusBtn'):
            DelRow(temp_group_scope_of_work, int(request.form.get('CommissioningScopeMinusBtn')))
            return redirect(url_for('manpower_page'))

    ### Planner
       ### 5-day-week TODO 6-day-week
       ### Plus-button by date   
        if request.form.get('PlannerPlusBtnDate'): 
            # print(request.form)
            planner_output = request.form
            ### calculating workdays. for further infos https://pypi.org/project/python-networkdays/
            calc_networkdays = workdays.networkdays(datetime.strptime(planner_output['date_start'], '%Y-%m-%d'), datetime.strptime(planner_output['date_stop'], '%Y-%m-%d'))#-1)
            # list_workdays = networkdays.Networkdays(datetime.strptime(planner_output['date_start'], '%Y-%m-%d'),
            #                                      datetime.strptime(planner_output['date_stop'], '%Y-%m-%d'))
            if 'staff_from_temp' not in planner_output:
                flash(f'Choose and add a staff member', category='danger')
            elif 'scopes_from_temp' not in planner_output:
                flash(f'Choose and add a scope', category='danger')
            else:
                db.session.add(temp_planner(scope = planner_output['scopes_from_temp'],
                                            staff = planner_output['staff_from_temp'],
                                            start = planner_output['date_start'],
                                            stop  = planner_output['date_stop'],
                                            stop_workdays = calc_networkdays,#list_workdays.networkdays()),
                                            workdays= calc_networkdays))#list_workdays.networkdays())))#rep. amount of workdays
                db.session.commit()
            return redirect(url_for('manpower_page'))

       ### Plus-button by workdays
        if request.form.get('PlannerPlusBtnWorkdays'): 
            # print(request.form)
            planner_output = request.form
            ### calculating workdays. for further infos https://pypi.org/project/workdays/
            dateby_workdays = workdays.workday(datetime.strptime(planner_output['date_start'], '%Y-%m-%d'), int(planner_output['workdays_stop']))#-1)
            if 'staff_from_temp' not in planner_output:
                flash(f'Choose and add a staff member', category='danger')
            elif 'scopes_from_temp' not in planner_output:
                flash(f'Choose and add a scope', category='danger')
            else:
                db.session.add(temp_planner(scope = planner_output['scopes_from_temp'],
                                            staff = planner_output['staff_from_temp'],
                                            start = datetime.strptime(planner_output['date_start'], '%Y-%m-%d').strftime('%Y-%m-%d'),
                                            stop  = dateby_workdays.strftime('%Y-%m-%d'),
                                            stop_workdays = planner_output['workdays_stop'],
                                            workdays= planner_output['workdays_stop']#len(list_workdays.networkdays())
                                            #6-DAYWEEK -->   -(len(list_workdays.weekends())/2)
                                            ))
                db.session.commit()
            return redirect(url_for('manpower_page'))

       ### Textfield inline for workdays
        if request.form.get('PlannerWorkdayAdd-Value'): 
            # print(request.form)
            planner_tb_output = request.form
            temp_planner_row = temp_planner.query.filter_by(id=planner_tb_output['PlannerWorkdayAdd-ID']).first()
            ### calculating workdays. for further infos https://pypi.org/project/workdays/
            dateby_workdays = workdays.workday(datetime.strptime(temp_planner_row.start, '%Y-%m-%d'), int(planner_tb_output['PlannerWorkdayAdd-Value']))#-1)
            temp_planner_row.stop = dateby_workdays.strftime('%Y-%m-%d')
            temp_planner_row.stop_workdays = planner_tb_output['PlannerWorkdayAdd-Value']
            temp_planner_row.workdays = planner_tb_output['PlannerWorkdayAdd-Value']     
            db.session.commit()
            return redirect(url_for('manpower_page'))

       ### Minus button 
        if request.form.get('PlannerMinusBtn'):
            DelRow(temp_planner, int(request.form.get('PlannerMinusBtn')))
            return redirect(url_for('manpower_page'))

 ### Gantt diagram
  ### Create dataframe + filtering and sorting
    df= [dict(Task=0, Start='', Finish='', Resource='')]
    
    [df.append(dict(Task = i.scope,
                    Resource = i.staff,
                    Start = i.start,
                    Finish = i.stop)) for i in temp_planner.query.all() if not i.scope == 'Site management']

    if len(df)>=2:
        df = list(filter(lambda i: i['Task'] != 0, df))
    '''Sorts Planner-items by Start-date and Finish-date'''
    df = sorted(df, key=lambda k: (k['Start'],k['Finish']), reverse=True)

  ### Seperation of Site mangement, what allows to push it to the top of the gantt chartt
    [df.append(dict(Task = i.scope,
                        Resource = i.staff,
                        Start = i.start,
                        Finish = i.stop)) for i in temp_planner.query.all() if i.scope == 'Site management']

  ### Create Gantt diagram
    fig = ff.create_gantt(df, 
                          showgrid_x=True,
                          showgrid_y=True,
                          show_colorbar=True,
                          index_col='Resource',
                          group_tasks=False)#group_tasks=True,

  ### Gantt diagram settings
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                       'plot_bgcolor':'rgba(52,58,64,55)',#rgba(255,255,255,100)',#
                       'font_color':'white',
                       'font_size': 16,
                       'xaxis':dict(title='Days', tickformat="%d", tickmode = 'linear', dtick=86400000,rangebreaks=[dict(bounds=["sat", "mon"])]),
                    #    'xaxis2':go.XAxis(),
                    #    'xaxis2':dict(title='Days', tickformat="%d", tickmode = 'linear', dtick=86400000,rangebreaks=[dict(bounds=["sat", "mon"])], side='top'),
                    #    'xaxis':dict(title='CW', tickformat="%V", dtick=86400000*7, tickmode = 'linear', tickson="boundaries",rangebreaks=[dict(bounds=["sat", "mon"])]),#%d-%m604800000
                       'grid_ygap':1, 
                       'grid_columns':1,
                    #    'bargap':0.5,
                    #    'bargroupgap':0.5
                       })

  ### Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

 ### return-statement
    return render_template('manpower_calc.html', manpower_form=manpower_form,
                                                 staff_form=staff_form,
                                                 staff_items=staff_items, 
                                                 temp_group_scope_of_work_items=temp_group_scope_of_work_items,
                                                 temp_planner_items=temp_planner_items,
                                                 project_info_items=project_info_items,
                                                 graphJSON=graphJSON,
                                                 unplanned_scopes=unplanned_scopes)

@app.route('/costs', methods=['POST', 'GET'])
def costs_page():
    if len(temp_project_info.query.all()) == 0:
       flash(f"No project selected!", category='info')
       return redirect(url_for('home_page'))  
    project_info_items = temp_project_info.query.all()
    temp_planner_items = temp_planner.query.all()

    class costs: 
        def __init__(self, staff, workdays): 
            self.staff = staff 
            self.workdays = workdays
    
    costs_staff = []
    [costs_staff.append(costs(k.staff.split(" / ")[0], 
                              k.workdays)) for k in temp_planner_items if 
                                           k.staff.split(" / ")[0] not in costs_staff]
    print([k.staff for k in costs_staff])
    return render_template('costs.html', project_info_items = project_info_items,
                                         costs_staff = costs_staff)

### User administration

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
