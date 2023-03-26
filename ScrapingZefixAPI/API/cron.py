from email.mime import base

from six import add_metaclass
from .scrap.scrap import scrapZefix
from django.utils import timezone
from django.core.mail import EmailMessage
from .models import firms
from .word import fileManager
from os.path import join
import os
from ScrapingZefixAPI.settings import APP_DICT, BASE_DIR 



def getFirms():
    a = scrapZefix()
    a.get_firms_of_the_day()


def create_files():
    files = fileManager()
    files.get_zip_daily()


def daily_mail(delta=1):
    yesterday = timezone.now() - timezone.timedelta(delta)
    str_yesterday = str(yesterday).split()[0]
    day = yesterday.day
    weekday = APP_DICT['FR']['WEEKDAYS'][yesterday.weekday()]
    month = APP_DICT['FR']['MONTHS'][yesterday.month-1]
    year = yesterday.year
    all_dir_path = join(BASE_DIR, 'Static', str_yesterday)
    message = EmailMessage()
    
    message.subject = 'Nouvelles entreprises - %s %s %s %s'%(weekday, day, month, year)
    message.body = '''
    Bonjour !

    Vous trouverez en pièce jointe le PDF et les Words correspondant aux %i entreprises crées hier.

    Si une erreur apparaît dans un document, veuillez le notifier à scraping.rc@affluence.ch.

    Bien cordialement,
    Toute l'équipe Affluence
    '''%(firms.objects.filter(date__exact=str_yesterday).count())
    message.to = ['jeanbaptiste.conan.jbc@gmail.com','contact@affluence.ch']
    message.from_email = 'noreply@affluence.ch'

    message.attach_file(join(all_dir_path,'%s.pdf'%str_yesterday)), message.attach_file(join(all_dir_path,'%s.zip'%str_yesterday))
    message.send()



def purge():
    twodaysbefore = str(timezone.now() - timezone.timedelta(2)).split()[0]
    os.system('rm -rf %s'%join('Static', twodaysbefore))
    return True
