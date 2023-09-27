import netsnmp
import re


def main():
    host = input("Input the IP: ") # 10.7.20.4
    community = input("Input the community string: ") # HuaweiSNMP
    oid = '.1.3.6.1.2.1.1.1.0'
    print("")

    # obavlja snmpwalk
    oid = netsnmp.Varbind(oid)
    result = netsnmp.snmpget(oid, Version=2, DestHost=host, Community=community)
    result = result[0].decode()

    # Extract the model (second word)
    product = result.split()[1]

    # Extract the version (second word in the bracket)
    version_match = re.search(r'\((\w+ \w+)\)', result)
    version = version_match.group(1) if version_match else None
    version = version.split()[1][:-6]


if __name__=='__main__':
    main()