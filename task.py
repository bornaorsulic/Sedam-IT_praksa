import netsnmp


"""def snmpwalk(host, community, oid):
    oid_list = netsnmp.snmpwalk(netsnmp.Varbind(oid), Version=2, DestHost=host, Community=community)
    result = []
    for k in oid_list:
        result.append(k.decode('iso-8859-1', errors='replace'))

    return result 


if __name__ == "__main__":
    host = '10.7.20.1'
    community = 'junipersnmp'
    oid_to_walk = '.1.3.6.1.2'
    # .1.3.6.1.2.1.25.6.3.1

    walk_results = snmpwalk(host, community, oid_to_walk)

    for k in walk_results:
        if "JUNOS" in k:
            print(k)"""






def snmpwalk(host, community, oid):
    session = netsnmp.Session(DestHost=host, Version=2, Community=community)
    oid_list = netsnmp.VarList(netsnmp.Varbind(oid))

    results = session.walk(oid_list)
    return results


if __name__ == "__main__":
    host = '10.7.20.1'
    community = 'junipersnmp'
    oid_to_walk = '.1.3.6.1.2.1.25.6.3'

    walk_results = snmpwalk(host, community, oid_to_walk)

    for index, value in enumerate(walk_results):
        value_str = value.decode('iso-8859-1', errors='replace')
        if "JUNOS" in value_str:
            oid = f"{oid_to_walk}.{index + 1}"  # Construct the OID based on index
            print(f"OID: {oid}, Value: {value_str}")


