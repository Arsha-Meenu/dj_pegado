from rest_framework import serializers
from .models import StudentBase

class TransitionApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBase
        fields = ('status','user','name')
        # fields = ('__all__')
         