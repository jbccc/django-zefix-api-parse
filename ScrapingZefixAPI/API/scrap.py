from django import utils
import requests
from .models import Firms, Address
from django.test import TestCase
from django.utils import timezone

class scrapZefix():

    auth = ('jeanbaptiste.conan.jbc@gmail.com', 'tgVqA5hD')
    today = str(timezone.now()).split()[0]

    def __str__(self) -> str:
        return 'caca'
    def is_new_firm(self,publication):
        try:
            if publication['sogcPublication']["mutationTypes"][1]["id"] == 2:
                return True
            else:
                return False
        except:
            return False

    def get_admin(self, url, canton):

        return ''

    def add_to_table(self, firm):
        firm_info = firm['companyShort']

        #recover base info on the firm
        name = firm_info['name']
        CHE = firm_info['uid']
        form = firm_info['legalForm']['shortName']['de'] 

        #recover more info on the firm
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/uid/%s'%CHE
        more_firm_info = requests.get(url, auth=self.auth).json()[0]
         

        # recover address
        global_address = more_firm_info["address"]
        street = global_address['street']
        houseNumber = global_address['houseNumber']
        city = global_address['city']
        zip = global_address['swissZipCode']
        canton = more_firm_info["canton"]
        address = Address(nb = houseNumber, street = street, zip=zip, city=city)

        #recover admin
        url_to_get_admin = more_firm_info['cantonalExcerptWeb']
        admin = self.get_admin(url_to_get_admin, canton) 

        #save the address in db
        address.save()

        f = Firms(
            name=name,
            #form=form,
            CHE = CHE,
            canton = canton,
            address = address,
            admin = admin,
            date = self.today
        )
        f.save()
        return 'oui'


    def get_firms_of_the_day(self):
        #get the date of the day
        

        #scraping today's publication
        url = 'https://www.zefix.admin.ch/ZefixPublicREST/api/v1/sogc/bydate/%s'%self.today
        fosc_pub = requests.get(url, auth=self.auth).json()

        #filter only new firms
        new_firms = list(filter(self.is_new_firm, fosc_pub))

        #plug the infos of the new firms into the db
        new_firms_objects = list(map(self.add_to_table, new_firms))
        return new_firms_objects