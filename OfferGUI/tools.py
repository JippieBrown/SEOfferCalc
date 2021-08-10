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
    print(last_row)
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
    # print(filepath)
    RemoveTemporaryItems()
    with open(filepath) as fd:
            doc = xmltodict.parse(fd.read().encode("cp1252"))
    item = doc['form1']
    if 'V01.0920' in filepath:
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
        db.session.add(read_xml)
        db.session.commit()
        os.remove(filepath)
    elif 'V01.0420' in filepath:
        read_xml = temp_project_info(first_name               = item['Vorname'],
                                    last_name                = item['Nachname'],
                                    department               = item['Abteilung'],
                                    project_name             = item['ProjektName'],
                                    country                  = item['Projektland'],
                                    city                     = 'not readable',
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
                                    hv_plug_size             = 'not readable',
                                    remark                   = 'not readable',
                                    offer_until              = item['Block6']['DateField2'],
                                    kick_off_meeting         = item['Block6']['DateField3'],
                                    date_of_editing          = datetime.today())
        db.session.add(read_xml)
        db.session.commit() 
        os.remove(filepath)   
    else:
        flash(f"Wrong inquiry-xml version in filename", category='info')
        RemoveTemporaryItems()
        os.remove(filepath)
    return

def RemoveTemporaryItems():
    temp_project_info.query.delete()
    temp_staff.query.delete()
    temp_group_scope_of_work.query.delete()
    temp_planner.query.delete()
    db.session.commit()
    print("temp-tables emptied in local database!")
