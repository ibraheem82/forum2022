'''

# ===> ['serializer'] will be classes that take a certain model that we want to serialize or objects and it is going to turn it into a ['Json] data, and  then we can return that.
'''
from dataclasses import field
from rest_framework.serializers import ModelSerializer
from base.models import Room



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'