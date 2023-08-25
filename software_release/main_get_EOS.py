from get_table import getTableFromLink
from get_data import getDataFromTable
from get_software_release import getSoftwareReleases
from compare_the_data import compareData


def main():
    url = 'https://support.juniper.net/support/eol/software/junos/'
    hostname = '10.7.20.1'
    community = 'junipersnmp'
    """
    hostname = input("Input hostname(IP): ")
    community = input("Input community string: ")
    """

    getTableFromLink(url)

    with open('extracted_content.txt', 'r', encoding='utf-8') as file:
        table_content = file.read().strip()

    getDataFromTable(table_content)

    result = getSoftwareReleases(hostname, community)
    print(result)
    compareData(result)


if __name__ == '__main__':
    main()
