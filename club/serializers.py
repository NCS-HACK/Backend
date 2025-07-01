from rest_framework import serializers
from .models import User, Task, Event, File, Poll, Choice, Vote

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
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'last_accessed']
        


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    allowed_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Poll
        fields = ['id', 'question', 'description', 'created_by', 'is_active', 'allowed_users', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'choice']

    def validate(self, data):
        user = self.context['request'].user
        poll = data['poll']
        if Vote.objects.filter(poll=poll, user=user).exists():
            raise serializers.ValidationError("You have already voted on this poll.")
        if not poll.allowed_users.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not allowed to vote in this poll.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)