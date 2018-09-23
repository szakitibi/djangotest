from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post
# Add your serializers here.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'password',
                  'email',
                  'first_name',
                  'last_name',
                  'is_superuser')

    def create(self, validated_data):
        validated_data['is_superuser'] = 0  # no createsuperusers over REST
        user = User.objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    likes = serializers.ReadOnlyField()
    dislikes = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'
