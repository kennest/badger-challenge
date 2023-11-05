from rest_framework import serializers

from badger.models import *


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'image']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()

    class Meta:
        model = UserBadge
        fields = ['badge', 'date']


class UserSerializer(serializers.ModelSerializer):
    badges = UserBadgeSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'badges']
