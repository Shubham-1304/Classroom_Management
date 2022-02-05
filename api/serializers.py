import email
from rest_framework import serializers
#from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Register(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model=User
        fields=['email','username','password','password2']
        extra_kwargs={'password':{'write_only':True}}


    def save(self):
        user=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            )
        password=self.validated_data['password']
        password2=self.validated_data['password2']


        if password!=password2:
            raise serializers.ValidationError({'password':"Password doesn't match" })

        user.set_password(str(password))
        user.save()
        return user

class forgotPasswordSerializer(serializers.ModelSerializer):
    model=User
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
