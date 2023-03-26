import requests
import re
from bs4 import BeautifulSoup
from API.models import genderPerNames

def parsename(name:str):
    lastname = ''
    surname = ''
    name = name.split()
    full_name = 0
    lastname += name[0]
    name.pop(0)
    while not len(name)==0:

        if full_name:
            break


        elif genderPerNames.objects.filter(surname = name[0]).count()>=1:
            gender = genderPerNames.objects.filter(surname = name[0]).all()[0].gender
            full_name = 1
            surname = name[0] 
            name.pop(0)


        elif name[0].find('-')>-1:
            names = name[0].split('-')

            if genderPerNames.objects.filter(surname = names[0]).count()>=1:
                gender = genderPerNames.objects.filter(surname = names[0]).all()[0].gender
                full_name = 1
                surname = name[0]
                name.pop(0)

            elif genderPerNames.objects.filter(surname = names[1]).count()>=1:
                gender = genderPerNames.objects.filter(surname = names[1]).all()[0].gender
                full_name = 1
                surname = name[0]
                name.pop(0)

            else:
                lastname += ' ' + name[0]
                name.pop(0)

        else:
            lastname += ' ' + name[0]
            name.pop(0)

    if not full_name:
        gender = 2
    infos = (lastname, surname, gender)
    return infos

def ge_admin(url:str) -> str:
    
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    container = soup.find_all('a', text = re.compile('Fonctions'))[0]
    first_admin = container.findParent('tr').findNextSibling('tr').find_all('td')[0].text
    if first_admin.find(', de')>-1:
        return first_admin.split(', de')[0].replace('\n', '').replace('\r', '').replace('\t', '')
    elif first_admin.find(', du')>-1:
        return first_admin.split(', du')[0].replace('\n', '').replace('\r', '').replace('\t', '')
    elif first_admin.find(", d'")>-1:
        return first_admin.split(", d'")[0].replace('\n', '').replace('\r', '').replace('\t', '')
    else:
        return first_admin


def vd_admin(msg:str) -> str:
    announcment =[
        'Titulaire',
        'Gérant',
        'Associée-gérante',
        'Administration',
        'Associées-gérantes',
        'Associés-gérants',
        'Associé-gérant',
        'Associés-gérants',
        'Signature individuelle est conférée à ',
        'Associés',
    ]
    for way in announcment:
        if msg.find(way)==-1:
            continue
        #treat one particular case
        if way =='Signature individuelle est conférée à ':
            msg = msg.split(way)[1]
            if msg.find(', de')>-1:
                return msg.split(', de')[0]
            elif msg.find(', du')>-1:
                return msg.split(', du')[0]
            else:
                return msg

        #treat other cases
        else:
            msg = msg.split(way)[1]
            msg = msg.split(': ')[1]
            if msg.find(', de')>-1:
                return msg.split(', de')[0]
            elif msg.find(', du')>-1:
                return msg.split(', du')[0]
            elif msg.find(', d&apos;')>-1:
                return msg.split(', d&apos;')[0]
            else:
                return msg



    return 'ERROR\n ' + msg



if __name__=='__main__':
    url='https://ge.ch/hrcintapp/companyReport.action?companyOfsUid=CHE-401.121.016'
    print(ge_admin(url))