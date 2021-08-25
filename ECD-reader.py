import win32com.client
Selector = 'haukemaier@siemens-energy.com'
Fields = "sAMAccountName,otherPager,c,Manager,siemens-costLocationUnit,siemens-costLocation,mobile,physicalDeliveryOfficeName,msDS-PhoneticFirstName,sn,Title,Department,siemens-gid,mail"
query = "SELECT " + Fields + " FROM 'LDAP://ad101.siemens-energy.net:3268/DC=ad101,DC=siemens-energy,DC=net' WHERE mail='" + Selector + "'"
adoConn = win32com.client.Dispatch('ADODB.Connection')
adoConn.Provider="ADSDSOObject"
adoConn.Open('ADs Provider')
(adoRS, success) = adoConn.Execute(query)

# my_dict = {"Email":[],"Forename":[],"Surename":[],"Address":[]}
# my_dict["Forename"].append(adoRS.Fields('msDS-PhoneticFirstName').Value)

# print(my_dict)
# fields_dict = {}
# for x in range(adoRS.Fields.Count):
#     fields_dict[x] = adoRS.Fields.Item(x).Value
#     # print fields_dict[x], recordset.Fields.Item(x).Value
# print(fields_dict)
# print(adoRS.Fields('sAMAccountName').Value)
# print(adoRS.Fields('mobile').Value)
# print(adoRS.Fields('Department').Value)
# print(adoRS.Fields('physicalDeliveryOfficeName').Value)
# print(adoRS.Fields('msDS-PhoneticFirstName').Value)
# print(adoRS.Fields('sn').Value)
# print(adoRS.Fields('c').Value)
# print(adoRS.Fields('Manager').Value)
# print(adoRS.Fields('otherPager').Value)