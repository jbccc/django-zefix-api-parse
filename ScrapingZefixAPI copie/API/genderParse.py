import pandas as pd
from API.models import genderPerNames

def create_gender_db():
    file  = pd.read_excel('Static/Excel/names.xlsx')
    rows = file.iterrows()
    rows = list(rows)[5:-8]
    for row in rows:
        values = row[1].values
        if values[1] == '*':
            gender = 0
        elif values[2] == '*':
            gender = 1
        else:
            gender = 1 if values[1]>values[2] else 0
        try:
            genderPerNames.objects.create(surname = values[0], gender = gender)
        except:
            continue