from django.shortcuts import render
from .models import User, Task
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=204)

@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = UserSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)
    
    serializer = UserSerializer(task)
    return Response(serializer.data)

@api_view(['POST'])
def create_task(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save()
        return Response(UserSerializer(task).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = UserSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        task = serializer.save()
        return Response(UserSerializer(task).data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return Response(status=204)

@api_view(['GET'])
def user_tasks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = user.assigned_tasks.all()
    serializer = UserSerializer(tasks, many=True)
    return Response(serializer.data)

