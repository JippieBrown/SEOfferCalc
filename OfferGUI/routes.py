from OfferGUI import app, db
from OfferGUI.models import *
from OfferGUI.forms import *
from flask import render_template, redirect, request, url_for, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from OfferGUI.tools import AddRow, DelRow, XmlReader, RemoveTemporaryItems
import os
import xmltodict
@app.route('/costs', methods=['POST', 'GET'])
@login_required
def costs_page():
    print("yeah")
    if len(temp_inquiry.query.all()) == 0 and len(temp_project_info.query.all()) == 0:
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
            print("removed!")
            req_project_name = [request.form[key] for key in request.form.keys()][1]
            ### get row in collected projects by select field above 'load'
            project_row = collected_projects.query.filter_by(project_name=req_project_name).first()
            print(project_row.id)

            ### writing in database
            temp_project_infos = temp_project_info(project_name         = project_row.project_name        ,
                                                   project_manager_dept = project_row.project_manager_dept,
                                                   order_indicator      = project_row.order_indicator     ,
                                                   site                 = project_row.site                ,
                                                   customer             = project_row.customer            ,
                                                   calc_for             = project_row.calc_for            ,
                                                   date                 = project_row.date                ,
                                                   cost_determination   = project_row.cost_determination  ,
                                                   editor               = project_row.editor              ,
                                                   project_id           = project_row.project_id          ,
                                                   plant_type           = project_row.plant_type          ,
                                                   busbar               = project_row.busbar              ,
                                                   number_of_bays       = project_row.number_of_bays      ,
                                                   commissioning        = project_row.commissioning       )
            db.session.add(temp_project_infos)
            db.session.commit()
            return redirect(url_for('project_page'))
    return render_template('home.html', home_form=home_form)

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
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
        # class from from models-py
        dde = dropdown_elements
        # reading from database
        db_user = User.query.with_entities(User.username, User.username).all()
        db_plant_type = dde.query.with_entities(dde.plant_type, dde.plant_type).filter(dde.plant_type!="NULL")
        db_busbar = dde.query.with_entities(dde.busbar, dde.busbar).filter(dde.busbar!="NULL")
        db_calc_for = dde.query.with_entities(dde.calc_for, dde.calc_for).filter(dde.calc_for!="NULL")
        db_yes_no = dde.query.with_entities(dde.yes_no, dde.yes_no).filter(dde.yes_no!="NULL")
        db_languages = dde.query.with_entities(dde.languages, dde.languages).filter(dde.languages!="NULL")
        db_temp_inquiry = temp_inquiry.query.all()
        temp_project_info.query.all()
        # setting choices (forms.py --> class ProjectForm)
        form.calc_for.choices = [k for k in db_calc_for]
        form.editor.choices = [k for k in db_user]
        form.plant_type.choices = [k for k in db_plant_type]
        form.busbar.choices = [k for k in db_busbar]
        form.commissioning.choices = [k for k in db_yes_no]
        form.site_management.choices = [k for k in db_yes_no]
        form.manpower.choices = [k for k in db_yes_no]
        form.manpower_language.choices = [k for k in db_languages]
        form.tools.choices = [k for k in db_yes_no]

        if len(temp_project_info.query.all()) == 1:
            item = temp_project_info.query.get(1)
            #set data on project info page
            form.editor.data                = item.editor
            form.project_name.data          = item.project_name
            form.project_manager_dept.data  = item.project_manager_dept
            form.order_indicator.data       = item.order_indicator
            form.site.data                  = item.site
            form.customer.data              = item.customer
            form.calc_for.data              = item.calc_for
            form.date.data                  = datetime.strptime(item.date, '%Y-%m-%d')
            form.cost_determination.data    = datetime.strptime(item.cost_determination, '%Y-%m-%d')
            form.editor.data                = item.editor
            form.project_id.data            = item.project_id
            form.number_of_bays.data        = item.number_of_bays
            form.plant_type.data            = item.plant_type
            form.busbar.data                = item.busbar
            form.commissioning.data         = item.commissioning
            # form.manpower.data              = item.manpower
            # form.manpower_language.data     = item.manpower_language
            # form.tools.data                 = item.tools      
              
        # setting data by imported xml-file (forms.py --> class ProjectForm)
        elif len(temp_inquiry.query.all()) == 1:
            #get temp inquiry info from database
            item = temp_inquiry.query.get(1)
            #set data on project info page
            form.editor.data                = current_user.username
            form.project_name.data          = item.project_name
            form.project_manager_dept.data  = item.firstname + " " + item.lastname + " / " + item.department
            form.site.data                  = str(item.city) + ", " + str(item.country)
            form.calc_for.data              = item.calc_for
            form.number_of_bays.data        = item.number_of_bays
            form.plant_type.data            = item.plant_type
            form.busbar.data                = item.busbar
            form.date.data                  = datetime.today()
            if item.offer_until != None:
                form.cost_determination.data    = datetime.strptime(item.offer_until, '%Y-%m-%d')
            form.commissioning.data         = item.commissioning
            form.manpower.data              = item.mpd
            form.manpower_language.data     = item.language
            form.tools.data                 = item.tools
        elif len(temp_inquiry.query.all()) == 0 and len(temp_project_info.query.all()) == 0:
            flash(f"No project selected!", category='info')
            return redirect(url_for('home_page'))            
        elif len(temp_inquiry.query.all()) >= 2:
            RemoveTemporaryItems()
            flash(f"Database table 'temp_inquiry' emptied, try again!", category='info')
            return redirect(url_for('home_page'))
        return render_template('project_info.html', form=form, save_form=save_form)

    if save_form.validate_on_submit():
        # project_info_col = [attr for attr in dir(project_info) 
        #                             if not attr.startswith("_") 
        #                             and attr not in ['Save project!','metadata','query','query_class']]
        project_output = [request.form[key] for key in request.form.keys()]
        # print(project_output)
        if len(project_output) >= 1:
            # writing in database
            project_infos = collected_projects(project_name         = project_output[2],
                                            project_manager_dept = project_output[3],
                                            order_indicator      = project_output[4],
                                            site                 = project_output[5],
                                            customer             = project_output[6],
                                            calc_for             = project_output[7],
                                            date                 = project_output[8],
                                            cost_determination   = project_output[9],
                                            editor               = project_output[10],
                                            project_id           = project_output[11],
                                            plant_type           = project_output[12],
                                            busbar               = project_output[13],
                                            number_of_bays       = project_output[14])
            #temp data needed for cost page
            # temp_project_infos = temp_project_info(project_name=project_output[2],
            #                                        calc_for=project_output[7],
            #                                        editor=project_output[10],
            #                                        project_id=project_output[11],)
            temp_project_infos = temp_project_info(project_name         = project_output[2],
                                                project_manager_dept = project_output[3],
                                                order_indicator      = project_output[4],
                                                site                 = project_output[5],
                                                customer             = project_output[6],
                                                calc_for             = project_output[7],
                                                date                 = project_output[8],
                                                cost_determination   = project_output[9],
                                                editor               = project_output[10],
                                                project_id           = project_output[11],
                                                plant_type           = project_output[12],
                                                busbar               = project_output[13],
                                                number_of_bays       = project_output[14]) 
            temp_project_info.query.delete()
            db.session.commit()
            db.session.add(project_infos)
            db.session.add(temp_project_infos)
            db.session.commit()
            flash(f"Data from project page stored in database!", category='success')


            # project_output = [[request.form[key] for key in request.form.keys() if key == i] for i in project_info_col]
            # print(project_output)

            # for attr, value in project_info.__dict__.items():
            #     attr = project_info_col[i]
            #     value = project_output[i]

            # for i,j in zip(project_info_col, project_output):
            #     project_infos = project_info.__dict__.keys

            return redirect(url_for('costs_page'))
    if save_form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('project_info.html', form=form, save_form=save_form)