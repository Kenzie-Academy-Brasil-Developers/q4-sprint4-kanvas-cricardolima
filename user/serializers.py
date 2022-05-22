from rest_framework import serializers

class UsersSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    is_admin = serializers.BooleanField(required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()