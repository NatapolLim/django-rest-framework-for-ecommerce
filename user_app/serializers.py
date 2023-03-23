
from rest_framework import serializers
from .models import Profile

from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    class Meta:
        model = Profile
        fields = ['url', 'id', 'user', 'image', 'address']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    profile = ProfileSerializer(read_only=True)
    # orderitem2user = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='orderitem-detail')
    order2user = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='order-detail')

    def validate(self, data):
        method = self.context['request'].method
        password = data.get('password', None)
        if method=='POST':
            if password==None:
                raise serializers.ValidationError({'info':'Please provide a password.'})
        elif method=='PUT' or method=='PATCH':
            old_pass = data.get('old_password', None)
            if password!=None and old_pass==None:
                raise serializers.ValidationError({'info':'Please provide a old password for changing password'})
            elif password==None and old_pass!=None:
                raise serializers.ValidationError({'info':'Please provide a password for changing password'})
        return data


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                old_pass = validated_data.pop('old_password')
                password = validated_data.pop('password')
                if user.check_password(old_pass):
                    user.set_password(password)
                else:
                    raise Exception('Old password is incorrect.')
                user.save()
        except Exception as err:
            raise serializers.ValidationError({'info': err})
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = ['url', 'profile', 'id', 'email', 'username', 'old_password',
                  'password', 'first_name', 'last_name', 'order2user']



        