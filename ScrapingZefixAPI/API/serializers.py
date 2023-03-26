from rest_framework import serializers

class legalForm(serializers.Serializer):
    name=serializers.CharField(max_length=10)

class canton(serializers.Serializer):
    name=serializers.CharField(max_length=2)

if __name__=="__main__":
    s = canton({'name':"VD"})
    print(s)