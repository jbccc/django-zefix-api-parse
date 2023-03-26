from django.db import models
from django.contrib.auth.models import User

class firm_admin(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=200)
    class genderType(models.IntegerChoices):
        MALE = 0
        FEMALE = 1
        undefined = 2
    gender = models.IntegerField(choices=genderType.choices)

    def __str__(self):
        return self.lastname + self.surname

class firms(models.Model):

    legal_form = [
        ('SA', 'Société anonyme'),
        ('SARL', 'Société à responsabilité limitée'),
        ('EI', 'Entreprise individuelle'),
    ]

    name = models.CharField(max_length=200, primary_key=True)
    CHE = models.CharField(max_length=15)
    date = models.DateField()
    canton = models.CharField(max_length=10)
    form = models.CharField(max_length=5, choices=legal_form)

    #admin field, pointing to the admin in the admin table, delete the firm if the admin is deleted as well
    admin = models.ForeignKey(firm_admin, on_delete=models.CASCADE)

    #address of the firm
    street = models.CharField(max_length=50)
    nip = models.IntegerField(default=0)
    city = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    
class words(models.Model):
    language=[
        ('FR', 'French'),
        ('EN','English'),
        ('DE','German'),
    ]
    name=models.CharField(max_length=50)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    filepath = models.FileField(upload_to="Static/privateFiles")
    lang=models.CharField(max_length=2, choices=language)

class genderPerNames(models.Model):
    surname = models.CharField(max_length=50, primary_key=True)
    class genderType(models.IntegerChoices):
        MALE = 0
        FEMALE = 1

    gender = models.IntegerField(choices=genderType.choices)

    def __str__(self) -> str:
        return self.surname


class failed_to_parse(models.Model):
    name = models.CharField(max_length=500)
    uid = models.CharField(max_length=500)
    date = models.DateField()



class words(models.Model):
    name=models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='usersfile')