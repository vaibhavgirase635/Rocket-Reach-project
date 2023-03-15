from rest_framework import serializers
from .models import CustomUser
from .models import *
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'email', 'password', 'confirm_password')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data


    def create(self, validated_data):
        user = CustomUser(full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




# User Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields= ['id','full_name','stream','school','degree','job_title','skills','experiance','company','phone','email','linkdin','Twitter','github','alt_phone','gender','DOB','location','profile_photo','created_at','updated_at']



#Overriding AuthTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Pricing_Plan
        fields = ['tokens','subscription','created_at','updated_at']

class Purchased_Subcription_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Purchased_Subcription
        fields = ['user_name','subscription']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tokens
        fields = ['user','tokens']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'specifications']