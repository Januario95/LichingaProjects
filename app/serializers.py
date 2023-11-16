from rest_framework import serializers

from .models import (
    Expense, Project, Employee, Quantity
)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        depth = 2

