
from .models import Packages
from rest_framework import serializers

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'