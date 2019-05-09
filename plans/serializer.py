from rest_framework import serializers
from .models import Plan, PlanFeature



class PlanFeatureSerializer(serializers.ModelSerializer):
    """Serializer to map the PlanFeature Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = PlanFeature
        fields = ('display_text','created_at')

    
class PlanSerializer(serializers.ModelSerializer):
    """Serializer to map the Plan Model instance into JSON format."""
    features = PlanFeatureSerializer(many=True)

    class Meta:
        model = Plan
        fields = ('plan_name', 'description', 'amount','currency','period', 'interval','notes', 'features')
    #StringRelatedField may be used to represent the target of the relationship using its __str__ method.
    #Nested relationships can be expressed by using serializers as fields

    def create(self, validated_data):
        #features_data - is added to support nested feature set under plan
        #refer to writable nested 
        features_data = validated_data.pop('features')
        planObj = Plan.objects.create(**validated_data)
        for feature_data in features_data:
            PlanFeature.objects.create(plan=planObj, **feature_data)
        return planObj

    def update(self, instance, validated_data):

        instance.plan_name = validated_data.get('plan_name', instance.plan_name)
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.period = validated_data.get('period', instance.period)
        instance.interval = validated_data.get('interval', instance.interval)
        instance.notes = validated_data.get('notes', instance.notes)
        #instance.features = validated_data.get('features', instance.features)
        instance.save()
        return instance

# class PlanSerializer(serializers.Serializer):
#     """Serializer to map the Plan Model instance into JSON format."""

#     plan_name = serializers.CharField(max_length=300)
#     description = serializers.CharField()
#     amount = serializers.IntegerField()
#     currency = serializers.CharField(max_length=3)
#     period = serializers.CharField(max_length=7)
#     interval = serializers.IntegerField()
#     notes = serializers.CharField(max_length=300, allow_blank=True)
    
#     #StringRelatedField may be used to represent the target of the relationship using its __str__ method.
#     #Nested relationships can be expressed by using serializers as fields

#     features = PlanFeatureSerializer(many=True)
