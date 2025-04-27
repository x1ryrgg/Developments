from rest_framework import serializers
from .models import *




class TreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreeStore
        fields = ('id', 'type', 'parent')
