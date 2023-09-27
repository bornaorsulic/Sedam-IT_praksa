import netsnmp
import re


def main():
    host = '10.7.20.18'
    host = input("Input hostname(IP): ")
    oid = '.1.3.6.1.2.1.1.1'
    community = 'hpesnmp'
    # .1.3.6.1.2.1.47.1.1.1.1.2.1 = STRING: "HPE Series Router MSR3012"
    # .1.3.6.1.2.1.47.1.1.1.1.11.1 = STRING: "CN9BK1Q08C"
    # .1.3.6.1.4.1.25506.8.35.18.4.3.1.6.0.0 = STRING: "7.1.059 Release 0306P30"

    # snmpwalk
    oid = netsnmp.Varbind(oid)
    results = netsnmp.snmpwalk(oid, Version=2, DestHost=host, Community=community)
    string_results = []
    for result in results:
        result = result.decode('iso-8859-1')
        string_results.append(result)

    string_results = string_results[0]

    # za ovaj host moze se iz uredaja izvuci device model, software version i release version
    if '10.7.20.3' == host:
        device_model_match = re.search(r'\nHPE\s+(\S+)', string_results)
        if device_model_match:
            device_model = device_model_match.group(1)

        # Extract Software Version using a regular expression
        software_version_match = re.search(r'Software Version\s+(\S+)', string_results)
        if software_version_match:
            software_version = software_version_match.group(1)[:-1]

        # Extract Release Version using a regular expression
        release_version_match = re.search(r'Release\s+(\S+)', string_results)
        if release_version_match:
            release_version = release_version_match.group(1)

        print("Device Model:", device_model)
        print("Software Version:", software_version)
        print("Release Version:", release_version)
    
    # za ovaj host uredaji su u obliku di se moze iz njih izvuci device model i software version
    elif '10.7.20.18' == host:

        # Extract Device Model and Product ID
        device_model_match = re.match(r'HPE (.+ J\d+)', string_results)
        if device_model_match:
            device_model = 'HPE' + device_model_match.group(1)

        # Extract Software Version
        software_version_match = re.search(r'PT\.([\d\.]+)', string_results)
        if software_version_match:
            software_version = 'PT.' + software_version_match.group(1)

        print("Device Model:", device_model)
        print("Software Version:", software_version)


if __name__=='__main__':
    main()
