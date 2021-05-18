import os
import xmltodict
from OfferGUI.models import *
from OfferGUI.forms import *
from OfferGUI import db
from datetime import datetime
from flask import render_template, redirect, request, url_for, flash, get_flashed_messages
def AddRow(table, items, unitprice, sum_item):

    item_to_create = table(Service=items[1],
                           RentalMode=items[3],
                           RentalUnits=items[2],
                           Remark=items[4],
                           UnitPrice=unitprice,
                           Sum=sum_item)
    db.session.add(item_to_create)
    db.session.commit()

def DelRow(table, id_row):
    last_id = id_row#len(table.query.all())
    last_row = table.query.get(last_id)
    if last_id >= 1:
        db.session.delete(last_row)
        db.session.commit()
    else:
        flash(f"Table empty!", category='warning')

def XmlReader(filepath):
    '''
    Reads xml-File by 'filepath'
    Uses '.encode("cp1252")' to pass ÖÄÜöäüß
    Writes in database table 'temp_project_info'
    '''
    with open(filepath) as fd:
            doc = xmltodict.parse(fd.read().encode("cp1252"))
    item = doc['form1']
    # print(doc['form1']['DateField1'])
    read_xml = temp_project_info(first_name               = item['Vorname'],
                                 last_name                = item['Nachname'],
                                 department               = item['Abteilung'],
                                 project_name             = item['ProjektName'],
                                 country                  = item['Projektland'],
                                 city                     = item['TextField5'],
                                 inquiry_date             = item['DateField1'],
                                 plant_type               = item['Anlagentyp'],    
                                 validity                 = item['Gueltigkeit'],
                                 protection_class_indoor  = item['Schutzkl_1'],
                                 protection_class_outdoor = item['Schutzkl_2'],
                                 calc_for                 = item['Angebot'],
                                 busbar                   = item['SaS'],
                                 number_of_bays           = item['Anzahl'],
                                 supervision              = item['Block1']['Bauleiter'],
                                 commissioning            = item['Block1']['IBSler'],
                                 mpd                      = item['Block1']['MPD_2'],
                                 language                 = item['Block1']['DropDownlist11'],
                                 tools                    = item['Block2']['Werkzeug_2'],
                                 hv_test_equipment        = item['Block2']['HV-Test_2'],
                                 transport                = item['Block3']['Transport_2'],
                                 sec_works                = item['Block4']['Sekundaer_2'],
                                 sec_works_no_of_bays     = item['Block4']['Felder_Zahl1'],
                                 earthing                 = item['Block4']['Erdung_2'],
                                 pd_measurement           = item['Block5']['DropDownList28'],
                                 psd                      = item['Block5']['PSD2'],
                                 actas                    = item['Block5']['ACTAS2'],
                                 libo                     = item['Block5']['LIBO_2'],
                                 customer_training        = item['Block5']['Training_2'],
                                 indoor_crane             = item['Block6']['Hallenkran_2'],
                                 dc_supply                = item['Block6']['DC_versorgung_2'],
                                 hv_plugs                 = item['Block6']['HS_Kabel_2'],
                                 hv_plug_size             = item['Block6']['Kabelsteckbuchsen'],
                                 remark                   = item['Block6']['Bemerkung'],
                                 offer_until              = item['Block6']['DateField2'],
                                 kick_off_meeting         = item['Block6']['DateField3'],
                                 date_of_editing          = datetime.today())

    RemoveTemporaryItems()
    db.session.add(read_xml)
    db.session.commit()
    os.remove(filepath)
    return

def RemoveTemporaryItems():
    temp_project_info.query.delete()
    temp_staff_costs.query.delete()
    temp_tool_costs.query.delete()
    db.session.commit()

def SelectFieldSetter(form):
    '''
    Reading dropdown elements from database
    and setting choices in frontend
    '''
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
            form.offer_date.data               = datetime.strptime(item.offer_date, '%Y-%m-%d')    
        form.editor.data                   = item.editor       

    elif len(temp_project_info.query.all()) == 0:
        flash(f"No project selected!", category='info')
        return redirect(url_for('home_page'))  