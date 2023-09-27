# Network Device Software and End-of-Life Data Scraper

## Huawei_snmp_get.py
Ovaj file će odraditi snmpwalk za Huawei Host, treba se unijeti Host IP, community string i program će izvući ime proizvoda i versiju koju koristi. Nadalje sa tim se može otići u tablicu sa svim uredajima i može se naći točno određeni datumi za taj proizvod i njegovu verziju
- ovaj file bi se trebao pokrenuti u linuxu jer snmp bolje radi tamo nego na windowsu


## scrape_data.py
Ovaj file će otići na stranicu od Huawei-a di se nalaze EOM i EOS datumi za svaki uređaj i verziju koju Huawei nudi 
    - `parsingSoftwareVersionWebsite()` je funkcija koja će pozivati funkciju `getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, first)`
    - `getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, first)` je funkcija koja će otići na stranicu i screjpati sve datume za sve ponuđene versions tako da ovisno šta smo joj dali od argumenata: dropdown_xpath(317-323) je samo Xpath od glavne kucice "Enter directly or click the arrow on the right" kako bi se pojavio dropdown izbornik. Prvo možemo vidjeti Product Family i među njima imamo Switches i Routers koje treba pretražiti, stoga sljedeći argument je first(305-315) koji je string "Switch", "Router" ili False, ako je "Switch" onda će program unijeti točku u kucicu da se izbornik otvori i da počne nuditi proizvode za prvi switch(Campus Switch), ako je "Router" onda će program kliknuti na rutere da se ponude razne vrste rutera i kada je False onda će provjeravati ostale vrste rutera ili ako je prije toga bilo u switchu. Nakon toga trebamo odabrati seriju(treba ih sve odabrati jednu po jednu) nakon koje ćemo moći kliknuti Confirm button i nakon toga Query button da se pojavi tablica. To je moguce tako da se odabere serija pa se onda proba izvrsit funkcija `ConfrimAndQuery(driver)`, ako to nije moguce onda postoje dva ishoda: 

        1. pojavi se model dropdown nakon kojega se opet pokušava izvršiti funkcija `ConfrimAndQuery(driver)`, ako uspije onda se pojavljuje tablica i vadi se iz nje informacije, ako ne znaci da je došlo do pogreške

        2. pojavi se subSeries dropdown nakon kojega se treba odabrati neki model koji će izači kao novi dropdown i onda se treba izvršiti funkcija `ConfrimAndQuery(driver)`

    **Svaki put kada ode u neki novi dropdown mora proci kroz cijelog njega(mora se nalazi u for loopu npr kao u mom kodu ili se može napraviti while loop koji povecava Xpath za 1 kroz svaku iteraciju i kada više ne može stisnuti novih modela, series ili subseries onda breaka iz while loopa)**

    - za taj dio di se mora odabrati pravi dropdown pomaze i funkcija productSubSeries(driver, subSeries, list_of_models)

    - kada se uspijela odraditi funkcija `ConfrimAndQuery(driver)` onda se pozove funkcija `scrapeData(driver, xpath_click)` koja pozove funkciju `getTableData(driver)` pa provjerava ima li tablica mogucnost da se promjeni stranica tablice, ako ima onda ode na novu stranicu i opet pozove funkciju `getTableData(driver)`, a ako nema to znači da je pogledao sve datume za odabrani series ili model

    - funkcija `getTableData(driver)` uz pomoc BeautifulSoup-a uzme html content of stranice i onda nađe di se nalazi tablica i uzme sve Products sa matching EOM i EOS datumom i to bi trebalo spremiti u Huawei_version_data.csv, unutar te funkcije nalazi se dio koji pregledava tablicu i gleda je li novi proizvod koji bi se dodao tablici mozda glupost koja nebi tamo trebala ic ili se podudara sa ostalim proizvodima i njihovim imenima. To radi funkcija `checkNewValues(csv_file_path, new_value)` 

    - funkcija `checkNewValues(csv_file_path, new_value)` koristi library fuzzywuzzy i gleda ako se string podudara za vise od 40 onda zapise taj Product u tablicu, inace ispise da se ne podudara i outputa taj proizvod pa da se to moze rucno provjeravati

Također ovaj file umjesto Software Versiona može uzeti i Product(Model) i njegove EOM i EOS datume, to rade funkcije `parsingProductWebsite()` koja je skoro identicna kao i `parsingSoftwareVersionWebsite()` i `getProduct(driver, dropdown_xpath, list_of_Xpaths, first)` koja je skoro identicna kao i `getSoftwareVersion(driver, dropdown_xpath, list_of_Xpaths, list_of_models, subSeries, first)`. Jedina razlika je što se koriste drugi Xpaths, drugi link stranice i drugi csv file(Huawei_Data.csv), sve ostalo je identicno.

Pozivanjem funkcija `parsingProductWebsite()` i `parsingSoftwareVersionWebsite()` dobit ce se dva csv file-a koja ce imati sve potrebne informacije. U slučaju da su csv files prazni onda treba za funkciju `checkNewValues(csv_file_path, new_value)` staviti da uvijek vraca True pa da spremi sve proizvode i vratiti tu funkciju kakva je prije bila pa da za u buduce ako se nesto promjeni ona odradi svoj posao.

## prototip1.py i prototip2.py
Ova dva file-a su nastali tako što sam spremio tu i tamo kod da ako se nešto zezne da imam stari kod koji djelomicno radi

## Known Issues
- Za pokretanje file-ova koji odrađuju snmpwalk ili snmpget treba se koristiti linux, a za ostale files Windows, ako se ti ostali files ne mogu runnat u Linuxu onda pokušajte staviti Headless option da ne otvara firefox.

