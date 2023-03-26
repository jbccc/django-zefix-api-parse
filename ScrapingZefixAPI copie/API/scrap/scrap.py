import requests
from API.models import firm_admin, firms, failed_to_parse
from django.utils import timezone
from API.scrap.scrap_admin import ge_admin, vd_admin, parsename

class scrapZefix():

    # auth for the zefix API
    auth = ("username", "password")
    # get yesterday's date, format YYYY-MM-DD, GMT+2 Europe/Zurich
    yesterday = str(timezone.now() - timezone.timedelta(1)).split()[0]

    def __str__(self) -> str:
        return self.yesterday


    def is_new_firm(self,publication) -> bool:
        try:
            # avoid certain companies
            if publication['companyShort']['legalForm']['id'] in [9,11,6,7]:
                return False
            #only VD and GE publication
            elif not publication['sogcPublication']['registryOfCommerceCanton'] in ['VD', 'GE']:
                return False
            # only new inscription
            elif publication['sogcPublication']["mutationTypes"][1]["id"] == 2:
                return True
            else: 
                return False
        #sometimes, publication['sogcPublication']["mutationTypes"][1] does not exist, try except to handle the error
        except:
            return False

    def get_admin(self, urlormessage: str, canton: str) -> str:
        if canton == 'VD':
            return vd_admin(urlormessage)
        elif canton == 'GE':
            url=urlormessage.replace('externalC', 'c')
            return ge_admin(url)
        else: 
            return ' '
        
    def add_to_table(self, firm):
        firm_info = firm['companyShort']
        message = firm['sogcPublication']['message']
        #recover base info on the firm
        name = firm_info['name'].replace('/', '-')
        CHE = firm_info['uid']
        form = firm_info['legalForm']['shortName']['fr']

        #recover more info on the firm
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/uid/%s'%(CHE)
        more_firm_info = requests.get(url, auth=self.auth).json()[0]
        

        # recover address
        global_address = more_firm_info["address"]
        street = global_address['street']
        houseNumber = global_address['houseNumber']
        city = global_address['city']
        nip = global_address['swissZipCode']
        canton = more_firm_info["canton"]

        #recover admin
        admin = self.get_admin(more_firm_info['cantonalExcerptWeb'], canton) if canton == 'GE' else  self.get_admin(message, canton)
        try : 
            admin = parsename(admin)
        except:
            failed_to_parse.save(name = name, uid = CHE, date = self.yesterday)
            return

        try : 
            admin = firm_admin(surname = admin[1], lastname = admin[0], gender = admin[2])
            admin.save()
        except:
            admin = firm_admin.objects.filter(surname__exact = admin[1]).all()[0]


        if firms.objects.filter(name__exact= name).count()>0:
            return

        f = firms(
            name=name,
            form = form,
            CHE = CHE,
            canton = canton,
            admin = admin,
            date = self.yesterday,
            street = street + ' ' + houseNumber,
            nip =  nip,
            city = city,
        )
        f.save()

    def test_parse_firm(self, firm):
        firm_info = firm['companyShort']
        message = firm['sogcPublication']['message']
        #recover base info on the firm
        name = firm_info['name'].replace('/', '-')
        CHE = firm_info['uid']
        form = firm_info['legalForm']['shortName']['fr']

        #recover more info on the firm
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/uid/%s'%(CHE)
        more_firm_info = requests.get(url, auth=self.auth).json()[0]
        

        # recover address
        global_address = more_firm_info["address"]
        street = global_address['street']
        houseNumber = global_address['houseNumber']
        city = global_address['city']
        zip = global_address['swissZipCode']
        canton = more_firm_info["canton"]

        #recover admin
        try : 
            admin = self.get_admin(more_firm_info['cantonalExcerptWeb'], canton) if canton == 'GE' else  self.get_admin(message, canton)
        except:
            # failed_to_parse.save(name = name, uid = CHE, date = self.yesterday)
            return 'nope'
        
        admin = parsename(admin)
        
        admin = firm_admin(surname = admin[1], lastname = admin[0], gender = admin[2])
        f = firms(
            name=name,
            form = form,
            CHE = CHE,
            canton = canton,
            admin = admin,
            date = self.yesterday,
            street = street + ' ' + houseNumber,
            zip =  zip,
            city = city,
        )
        return str(f.admin) + ' ' + CHE # for debug

    def get_firms_of_the_day(self): 
        #scraping yesterday's publication
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/sogc/bydate/%s'%self.yesterday
        fosc_pub = requests.get(url, auth=self.auth).json()

        #filter only new firms
        new_firms = list(filter(self.is_new_firm, fosc_pub))
        #plug the infos of the new firms into the db
        new_firms_objects = list(map(self.add_to_table, new_firms))
        # for firm in new_firms:
        #     self.add_to_table(firm)
        return new_firms_objects

    def test_scrap_firm_of_the_day(self): 
        #scraping yesterday's publication
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/sogc/bydate/%s'%self.yesterday
        fosc_pub = requests.get(url, auth=self.auth).json()

        #filter only new firms
        new_firms = list(filter(self.is_new_firm, fosc_pub))
        #plug the infos of the new firms into the db
        new_firms_objects = list(map(self.test_parse_firm, new_firms))

        return new_firms_objects

if __name__ == '__main__':
    a = scrapZefix()
    a.get_firms_of_the_day()