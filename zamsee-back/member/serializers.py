from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(allow_empty_file=True, allow_null=True)

    class Meta:
        model = User
        fields = (
            'nickname',
            'thumbnail',
        )
