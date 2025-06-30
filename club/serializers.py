from rest_framework import serializers
from .models import User, Task, Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_admin',
            'is_board',
            'department'
        ]
    
    
class TaskSerializer(serializers.ModelSerializer):
    # creator = UserSerializer()
    # assigned_to = UserSerializer()
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'assigned_to',
            'status',
            'due_date',
            'priority',
            'department',
            'creator',
        ]

class EventSerializer(serializers.ModelSerializer):
    # participants = UserSerializer(many = True)
    class Meta:
        model = Event
        fields = '__all__'