from rest_framework import serializers

from ..models import Payroll


class PayrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payroll
        fields = '__all__'


class PayrollReplenishSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    backURL = serializers.URLField(allow_blank=True)


class PayrollWithdrawSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    backURL = serializers.URLField(allow_blank=True)


class PayrollWithdrawRequestSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=128)
    card_number = serializers.IntegerField()


class PayrollUIDSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=128)


class PayrollBankUIDSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=128)
    bank = serializers.CharField(max_length=128)


class PayrollListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=('%d.%m.%Y, %H:%M'))
    card_number = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    payment_type = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = [
            'uid',
            'amount',
            'created_at',
            'payment_type',
            'comission_amount',
            'status',
            'card_number',
            ]

    def get_card_number(self, obj):
        if num := obj.card_number:
            num = str(num)
            return '{}-{}-{}-{}'.format(num[:4], num[4:8], num[8:12], num[12:])
        else:
            return 'не указана'

    def get_status(self, obj):
        return obj.get_status_display()

    def get_payment_type(self, obj):
        return obj.get_payment_type_display()
