from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense, Category


# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""

    class Meta:
        model = User
        fields = ("id", "username", "email")


# PUBLIC_INTERFACE
class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


# PUBLIC_INTERFACE
class LoginSerializer(serializers.Serializer):
    """Serializer for user authentication input."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# PUBLIC_INTERFACE
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category CRUD"""

    class Meta:
        model = Category
        fields = ("id", "name")


# PUBLIC_INTERFACE
class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for expenses"""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Expense
        fields = (
            "id", "amount", "date", "category", "category_id", "description", "created_at"
        )
