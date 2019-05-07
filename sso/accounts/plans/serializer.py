from rest_framework import serializers
from .models import Plan
from .models import PlanFeature

class PlanSerializer(serializers.Serializer):
    """Serializer to map the Plan Model instance into JSON format."""
    
    plan_name = serializers.CharField(max_length=300)
    description = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=3)
    period = serializers.CharField(max_length=7)
    interval = serializers.IntegerField()
    notes = serializers.CharField(max_length=300, allow_blank=True)

    def create(self, validated_data):
        return Plan.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.plan_name = validated_data.get('plan_name', instance.plan_name)
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.period = validated_data.get('period', instance.period)
        instance.interval = validated_data.get('interval', instance.interval)
        instance.notes = validated_data.get('notes', instance.notes)

        instance.save()
        return instance

class PlanFeatureSerializer(serializers.ModelSerializer):
    """Serializer to map the PlanFeature Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = PlanFeature
        fields = '__all__'


         