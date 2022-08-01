
from dataclasses import fields
from accounts.models import CustomUser, Profile
from rest_framework import serializers

from django.contrib.auth.models import AbstractUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password','first_name','email']
        extra_kwargs ={
            'password':{'write_only':True}
        }

    def save(self):
  
        account = CustomUser(
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            email = self.validated_data['email'],
        )

        password = self.validated_data['password']
        
        

        if not password:
            raise serializers.ValidationError({'password':"passwords must match"})

        account.set_password(password)
       
        account.save()
        return account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'email', 'is_staff', 'is_superuser', 'is_active')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Profile
        fields = ('id','full_name','get_profile_picture','email','username','phone','image','type','referral_code','user')
        
