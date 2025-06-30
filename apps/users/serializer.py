from rest_framework import serializers
from apps.users.models import User
from django.utils import timezone
import bcrypt


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)
    joined_at = serializers.DateTimeField(default=timezone.now, read_only=True)
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True, default=[])

    def create(self, validated_data):
        plain_password = validated_data.get("password").encode()
        # ---------- hash password ---------------
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password, salt)
        validated_data["password"] = hashed.decode()
        # ----------------------------------------
        return User.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.code = validated_data.get("code", instance.code)
    #     instance.linenos = validated_data.get("linenos", instance.linenos)
    #     instance.language = validated_data.get("language", instance.language)
    #     instance.style = validated_data.get("style", instance.style)
    #     instance.save()
    #     return instance
