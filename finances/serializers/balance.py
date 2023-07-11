from rest_framework import serializers


class BalanceSerializer(serializers.Serializer):
    secret_key = serializers.CharField(max_length=128)
