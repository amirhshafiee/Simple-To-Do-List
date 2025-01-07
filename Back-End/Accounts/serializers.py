from rest_framework import serializers
from .models import CustomUser

class RegisterCustomUserSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password', 'username']
        extra_kwargs ={
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError('passwords must be match ...')

        del validated_data['confirm_password']
        user = CustomUser.objects.create_user(
            **validated_data
        )

        return user


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name", "account_created_at"]
        extra_kwargs = {
            'account_created_at': {'read_only': True},
        }

class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()


    def validate(self, data):
        if data['new_password'] != data["confirm_new_password"]:
            raise serializers.ValidationError('Passwords must be match ...')
        return data