from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='full_name', max_length=150)
    phone = serializers.CharField(source='phone_number', max_length=20)
    poolSlug = serializers.SlugField(source='pool_slug', max_length=100, required=False, allow_null=True)
    poolName = serializers.CharField(source='pool_name', max_length=200, required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = ['id', 'fullName', 'phone', 'poolSlug', 'poolName', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_fullName(self, value):
        if not value.strip():
            raise serializers.ValidationError("ФИО не может быть пустым.")
        if len(value) > 150:
            raise serializers.ValidationError("ФИО слишком длинное (максимум 150 символов).")
        return value

    def validate_phone(self, value):
        cleaned = ''.join(c for c in value if c.isdigit() or c in '+-() ')
        digits = ''.join(c for c in cleaned if c.isdigit())
        if len(digits) < 10:
            raise serializers.ValidationError("Номер телефона должен содержать минимум 10 цифр.")
        return cleaned
        
    def validate(self, attrs):
        pool_name = attrs.get('pool_name')
        if not pool_name or pool_name.strip() == '':
            attrs['pool_name'] = 'Быстрая Связь'
        return attrs