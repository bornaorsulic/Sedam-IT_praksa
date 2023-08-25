import netsnmp
 

def getDataID(hostname, community):
    # -------------------------- treba oid stavit u function parameters
    OIDs = ['.1.3.6.1.4.1.2636.3.1.2.0', '.1.3.6.1.4.1.2636.3.63.1.1.1.2.1.3.59']
    # .1.3.6.1.4.1.2636.3.1.2.0 = STRING: "Juniper SRX550 Internet Router"
    # .1.3.6.1.4.1.2636.3.63.1.1.1.2.1.3.59 = STRING: "AX411 WLAN AP"
    # https://support.juniper.net/support/eol/product/srx_series/

    ID = []
    for OID in OIDs:
        oid = netsnmp.Varbind(OID)

        # Perform SNMP query
        result = netsnmp.snmpget(oid, Version=2, DestHost=hostname, Community=community)

        # Print the result
        if not result:
            print("No response(get_data_id.py is not working)")
        else:
            print(OID, " -> ", result[0].decode())

        if "Juniper" in result[0].decode():
            ID.append(result[0][8:14].decode())
        elif "WLAN" in result[0].decode():
            ID.append(result[0][0:5].decode())
    
    return ID
