import netsnmp


def getSoftwareReleases(hostname, community):
    """
    Retrieves the software release version of a network device using SNMP.

    Returns:
        str: The software release version of the network device (e.g., "Junos OS 18.2R3.4").

    This function uses SNMP to query a network device for its software release version.
    It specifies the hostname, community string, and OID to perform an SNMP query.
    If the query is successful, the software release version is extracted from the result
    and returned. If the query fails, an error message is printed.
    """

    OID = '.1.3.6.1.2.1.25.6.3.1.2.2' # treba jos oid dodat gore
    # .1.3.6.1.2.1.54.1.1.1.1.4.2
    # snmpwalk -v 2c -On -c junipersnmp  10.7.20.1  .1.3.6.1.2 | grep "JUNOS"
    oid = netsnmp.Varbind(OID)
    

    # Perform SNMP query
    result = netsnmp.snmpget(oid, Version=2, DestHost=hostname, Community=community)

    # Print the result
    if not result:
        print("No response(get_software_release.py is not working)")
    else:
        print(OID, " -> ", result[0].decode())

    software = 'Junos OS ' + result[0][24:31].decode()
    
    return software
