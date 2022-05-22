from rest_framework import serializers

from user.serializers import UsersSerializer

class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    house_number = serializers.IntegerField()
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    country = serializers.CharField()
    users = UsersSerializer(many=True, required=False)
    
class UserAddressSerializer(serializers.Serializer):
    address = AddressSerializer()